import assert from "node:assert/strict";
import { AllowanceBook } from "../src/local-simulator.js";

let now = 1_783_000_000;
const book = new AllowanceBook({ now: () => now });
const common = {
  ownerId: "user-wallet-1",
  agentId: "agent-coder-1",
  mint: "USDC",
};

const allowance = book.createFixedAllowance({
  ...common,
  totalUnits: 20_000_000,
  expiresAt: now + 604_800,
});

assert.equal(allowance.remainingUnits, 20_000_000);

book.pull({
  ...common,
  receiver: "pay.sh",
  amountUnits: 3_500_000,
  memo: "api-search",
});

book.pull({
  ...common,
  receiver: "rpc-provider",
  amountUnits: 9_000_000,
  memo: "indexing",
});

assert.equal(book.getAllowance(common).remainingUnits, 7_500_000);
assert.throws(
  () =>
    book.pull({
      ...common,
      receiver: "model-provider",
      amountUnits: 10_000_000,
      memo: "large-run",
    }),
  /allowance exceeded/,
);

book.revoke(common);

assert.throws(
  () =>
    book.pull({
      ...common,
      receiver: "pay.sh",
      amountUnits: 1_000_000,
      memo: "after-revoke",
    }),
  /allowance revoked/,
);

console.log("local simulator tests passed");
