import Lake
open Lake DSL

package «voynich-debunked» where
  name := "voynich-debunked"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.14.0"

lean_lib «VoynichProof» where
  srcDir := "."
  roots  := #[`voynich_proof]
