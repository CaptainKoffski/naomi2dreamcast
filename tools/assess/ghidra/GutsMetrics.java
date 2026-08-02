// GutsMetrics.java — Ghidra post-script: guts metrics for one Naomi boot image.
// args[0] = output JSON path. Ghidra 12.1.2 headless (Jython is gone; Java only).
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.scalar.Scalar;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class GutsMetrics extends GhidraScript {
    // {lo, hi} physical (addr & 0x1FFFFFFF). SCIF = SH4 on-chip serial 0xFFE8xxxx.
    static final long[][] MMIO = {
        {0x00710000L, 0x0071FFFFL},   // rtc: AICA RTC registers
        {0x01000000L, 0x01FFFFFFL},   // g2ext: G2 add-on board window (DIMM/net) — informational
        {0x1FE80000L, 0x1FE8FFFFL},   // scif
    };
    static final String[] MMIO_NAMES = {"rtc", "g2ext", "scif"};
    // Naomi BIOS syscall vectors. ../cleopatra/docs/kb/boot-binary.md names no
    // specific vector addresses (only the BIOS ROM range, phys 0x0-0x1fffff,
    // §7). The vector table itself is documented in
    // ../cleopatra/docs/kb/naomi-vs-dreamcast.md:328-331 (indirect vectors at
    // 0x8c0000b0 SYSINFO, 0x8c0000b4 ROM font, 0x8c0000b8 flashrom, 0x8c0000bc
    // misc+GD-ROM) and phase4-conversion.md:416 ("Vector pointers
    // 0x8c0000b0-0x8c0000e0"). 0x8c0000b4 (ROM font) added below per those docs.
    static final long[] BIOS_VEC = {0x8c0000b0L, 0x8c0000b4L, 0x8c0000b8L, 0x8c0000bcL, 0x8c0000c0L, 0x8c0000e0L};

    Map<String, Integer> mmio = new LinkedHashMap<>();
    Map<String, Integer> bios = new LinkedHashMap<>();

    void tally(long v) {
        long p = v & 0x1FFFFFFFL;
        for (int i = 0; i < MMIO.length; i++)
            if (p >= MMIO[i][0] && p <= MMIO[i][1])
                mmio.merge(MMIO_NAMES[i], 1, Integer::sum);
        for (long vec : BIOS_VEC)
            if (v == vec || p == (vec & 0x1FFFFFFFL))
                bios.merge(String.format("0x%08x", vec), 1, Integer::sum);
    }

    static String esc(String s) {
        StringBuilder b = new StringBuilder();
        for (char c : s.toCharArray()) {
            if (c == '"' || c == '\\') b.append('\\').append(c);
            else if (c >= 0x20 && c < 0x7f) b.append(c);
        }
        return b.toString();
    }

    @Override
    public void run() throws Exception {
        String[] scriptArgs = getScriptArgs();
        if (scriptArgs.length < 1) {
            throw new IllegalArgumentException(
                "GutsMetrics requires one arg: output JSON path (got " + scriptArgs.length + ")");
        }
        String outPath = scriptArgs[0];

        for (String n : MMIO_NAMES) mmio.put(n, 0);
        long codeBytes = 0;
        for (MemoryBlock b : currentProgram.getMemory().getBlocks())
            if (b.isInitialized()) codeBytes += b.getSize();
        int functions = currentProgram.getFunctionManager().getFunctionCount();

        InstructionIterator it = currentProgram.getListing().getInstructions(true);
        while (it.hasNext() && !monitor.isCancelled()) {
            Instruction ins = it.next();
            for (int op = 0; op < ins.getNumOperands(); op++)
                for (Object o : ins.getOpObjects(op))
                    if (o instanceof Scalar) tally(((Scalar) o).getUnsignedValue());
        }
        // SH4 reaches MMIO via literal pools -> defined 4-byte data and pointers
        List<String> strs = new ArrayList<>();
        DataIterator dit = currentProgram.getListing().getDefinedData(true);
        while (dit.hasNext() && !monitor.isCancelled()) {
            Data d = dit.next();
            Object v = d.getValue();
            if (d.getLength() == 4 && v instanceof Scalar)
                tally(((Scalar) v).getUnsignedValue());
            else if (v instanceof ghidra.program.model.address.Address)
                tally(((ghidra.program.model.address.Address) v).getOffset());
            else if (d.hasStringValue() && strs.size() < 500) {
                // ponytail: getValue() is the clean string; fall back to the
                // quote-wrapped display form only if getValue() isn't a String.
                String s = (v instanceof String) ? (String) v : d.getDefaultValueRepresentation();
                if (s.length() >= 10) strs.add(esc(s));
            }
        }

        try (PrintWriter w = new PrintWriter(outPath)) {
            w.printf("{\"code_bytes\": %d, \"functions\": %d,%n", codeBytes, functions);
            w.print("\"mmio_refs\": {");
            boolean first = true;
            for (Map.Entry<String, Integer> e : mmio.entrySet()) {
                if (!first) w.print(", ");
                w.printf("\"%s\": %d", e.getKey(), e.getValue()); first = false;
            }
            w.println("},");
            w.print("\"bios_refs\": {");
            first = true;
            for (Map.Entry<String, Integer> e : bios.entrySet()) {
                if (!first) w.print(", ");
                w.printf("\"%s\": %d", e.getKey(), e.getValue()); first = false;
            }
            w.println("},");
            w.print("\"sdk_strings\": [");
            for (int i = 0; i < strs.size(); i++)
                w.printf("%s\"%s\"", i == 0 ? "" : ", ", strs.get(i));
            w.println("]}");
        }
        println("GutsMetrics: wrote " + outPath);
    }
}
