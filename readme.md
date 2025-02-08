# IAS Princeton Computer Simulator



### Memory Details
- **Memory Size**: 1000 locations.
- **Negative Integers Representation**: Signed bit representation.

---
### File Details
- **memory.txt** : Represents 1000 memory locations in **real-time**.
- **registers.txt** : Represents all the registers in **real-time**

---

### Instruction Set

| **Opcode (8-bit)** | **Symbolic Representation** | **Description**                                                                 |
|---------------------|-----------------------------|---------------------------------------------------------------------------------|
| `00100001`          | `STOR M(X)`                | Transfers content of accumulator to memory location X.                          |
| `00000001`          | `LOAD M(X)`                | Transfers content of memory location X to the accumulator.                      |
| `00000100`          | `LOADMQ`                  | Transfers the content of the MQ register to the accumulator.                    |
| `00001101`          | `JUMPL M(X)`              | Unconditionally jump to the instruction at the left half of memory location X.  |
| `00001110`          | `JUMPR M(X)`              | Unconditionally jump to the instruction at the right half of memory location X. |
| `00001111`          | `JUMPL+ M(X)`             | Conditionally jump to the left half of memory location X if `AC >= 0`.          |
| `00010000`          | `JUMPR+ M(X)`             | Conditionally jump to the right half of memory location X if `AC >= 0`.         |
| `00000101`          | `ADD M(X)`                | Add contents of memory location X to the accumulator; result stored in `AC`.    |
| `00000110`          | `SUB M(X)`                | Subtract contents of memory location X from the accumulator; result stored in `AC`. |
| `00001011`          | `MUL M(X)`                | Multiply contents of memory location X by `MQ`; MSB in `AC`, LSB in `MQ`.       |
| `00001100`          | `DIV M(X)`                | Divide `AC` by memory location X; quotient in `MQ`, remainder in `AC`.          |
| `00001000`          | `LSH`                     | Multiply `AC` by 2, shifting left one bit position.                             |
| `00001001`          | `RSH`                     | Divide `AC` by 2, shifting right one bit position.                              |

---


### Custom ISA

| **Opcode (8-bit)** | **Symbolic Representation** | **Description**                                                                 |
|---------------------|-----------------------------|-----------------------------------------------------------------|
| `11111111`          | `HALT`                    | Stops the program.                                                             |
| `10000000`          | `LDIM V(X)`               | Load an immediate value X (12-bit positive) directly into the accumulator `AC`.     |
| `11000000`          | `ADIM V(X)`               | Add an immediate value X with the content in the accumulator `AC`.                  |
| `11100000`          | `SBIM V(X)`               | Subtract an immediate value X with the content in the accumulator `AC`.             |

---
### Assembler Usage 

```bash
python3 assembler.py <input filename> <output filename>
```
---
### Simulator Usage

```bash
python3 sim.py <input filename> <flags>
```
Flag : `-a` for executing all instructions without stopping

---
### Supported Programs

1. **Factorial Calculation**
2. **Sum of First N Natural Numbers**
3. **Greatest Common Divisor (GCD)**
4. **Power Calculation**
5. **Reverse a Number**
6. **Prime Number Checker**
7. **Fibonacci Sequence**
8. And Many More!
