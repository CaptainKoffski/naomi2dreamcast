# General checklist
This is checklist for the future ports to be tested against.
Not for initial general portability assessments.

## Static analysis
- [ ] No VMU operations
- [ ] No serial port writings
- [ ] No unnecessary sleeps

## Dynamic testing
- [ ] Runs on emulator (flycast)
- [ ] Runs on real hardware
  - [ ] Runs via VGA
  - [ ] Runs via Composite
  - [ ] Runs from GDEMU
  - [ ] Runs from serial port (Dreamshell)
  - [ ] Runs from GD-ROM
  - [ ] All paths are documented
  - [ ] All paths are executed