import { fileURLToPath } from "node:url";

export class AllowanceBook {
  constructor({ now = () => Math.floor(Date.now() / 1000) } = {}) {
    this.now = now;
    this.allowances = new Map();
    this.events = [];
  }

  createFixedAllowance({ ownerId, agentId, mint, totalUnits, expiresAt }) {
    assertPositive(totalUnits, "totalUnits");
    if (!ownerId || !agentId || !mint) {
      throw new Error("ownerId, agentId, and mint are required");
    }
    if (expiresAt <= this.now()) {
      throw new Error("expiresAt must be in the future");
    }

    const id = `${ownerId}:${agentId}:${mint}`;
    const allowance = {
      id,
      ownerId,
      agentId,
      mint,
      totalUnits,
      remainingUnits: totalUnits,
      expiresAt,
      revoked: false,
      pulls: [],
    };
    this.allowances.set(id, allowance);
    this.events.push({ type: "ALLOWANCE_CREATED", id, totalUnits, expiresAt });
    return allowance;
  }

  pull({ ownerId, agentId, mint, receiver, amountUnits, memo }) {
    assertPositive(amountUnits, "amountUnits");
    const allowance = this.getAllowance({ ownerId, agentId, mint });

    if (allowance.revoked) {
      throw new Error("allowance revoked");
    }
    if (allowance.expiresAt <= this.now()) {
      throw new Error("allowance expired");
    }
    if (amountUnits > allowance.remainingUnits) {
      throw new Error("allowance exceeded");
    }

    const pull = {
      receiver,
      amountUnits,
      memo,
      ts: this.now(),
      remainingAfter: allowance.remainingUnits - amountUnits,
    };
    allowance.remainingUnits -= amountUnits;
    allowance.pulls.push(pull);
    this.events.push({ type: "PULL", id: allowance.id, ...pull });
    return pull;
  }

  revoke({ ownerId, agentId, mint }) {
    const allowance = this.getAllowance({ ownerId, agentId, mint });
    allowance.revoked = true;
    this.events.push({ type: "ALLOWANCE_REVOKED", id: allowance.id, ts: this.now() });
    return allowance;
  }

  getAllowance({ ownerId, agentId, mint }) {
    const id = `${ownerId}:${agentId}:${mint}`;
    const allowance = this.allowances.get(id);
    if (!allowance) {
      throw new Error("allowance not found");
    }
    return allowance;
  }
}

function assertPositive(value, field) {
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error(`${field} must be a positive integer`);
  }
}

export function runDemo() {
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
    expiresAt: now + 7 * 24 * 60 * 60,
  });
  console.log(`created allowance: ${allowance.totalUnits} units for ${allowance.agentId}`);

  const first = book.pull({
    ...common,
    receiver: "pay.sh",
    amountUnits: 3_500_000,
    memo: "api-search",
  });
  console.log(`pull ok: ${first.receiver} ${first.memo} ${first.amountUnits}`);

  const second = book.pull({
    ...common,
    receiver: "rpc-provider",
    amountUnits: 9_000_000,
    memo: "indexing",
  });
  console.log(`pull ok: ${second.receiver} ${second.memo} ${second.amountUnits}`);

  try {
    book.pull({
      ...common,
      receiver: "model-provider",
      amountUnits: 10_000_000,
      memo: "large-run",
    });
  } catch (error) {
    console.log(`blocked: ${error.message}`);
  }

  book.revoke(common);
  console.log("revoked allowance");

  try {
    book.pull({
      ...common,
      receiver: "pay.sh",
      amountUnits: 1_000_000,
      memo: "after-revoke",
    });
  } catch (error) {
    console.log(`blocked: ${error.message}`);
  }

  console.log(`remaining allowance: ${book.getAllowance(common).remainingUnits}`);
  return book;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  runDemo();
}
