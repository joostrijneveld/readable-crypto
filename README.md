The goal of this repository is to provide readable implementations for various cryptographic algorithms. All contained code is provided for reference purposes; it is not efficient, not small and not secure. You should _never_ rely on these implementations in production environments (or in any other environment, really).

Instead, these implementations are aimed to be 'minimal working examples' that are concise, readable and easy to execute. Various unit tests are included for function-level testing, but the true strength lies in being able to compare each individual action with your own interpretation and implementation.

But most of all, this is the result of a bit of practice.

Currently this repository contains:

* Block ciphers
    * KLEIN (64-bit, 80-bit and 96-bit)
    * PRESENT (80-bit and 128-bit)
* Hash functions
    * QUARK (U-QUARK, D-QUARK and S-QUARK variants)
    * SPONGENT (88-bit, 128-bit, 160-bit, 224-bit, 256-bit)

Pull requests are appreciated, bearing in mind the above mentioned constraints.
