# Solana Native Subscriptions & Allowances Code Sample

Submission for Superteam Canada bounty:
https://superteam.fun/earn/listing/technical-demo-solana-native-subscriptions-and-allowances-code-sample

Author: Brandon Bounty
Last checked: June 9, 2026

## What This Demo Shows

This repo contains a small, focused code sample for the Solana Subscriptions & Allowances primitive. It models an "agent API budget" use case:

> A user gives an autonomous coding agent a capped weekly USDC allowance. The agent can pay approved API providers until the cap is exhausted or the period expires. The user can audit every pull and revoke the allowance.

The sample has two layers:

- `src/local-simulator.js`: runnable local simulation with no wallet, no RPC, no private keys, and no external dependencies.
- `src/sdk-flow.ts`: TypeScript adapter sketch using the official `@solana/subscriptions` SDK patterns for onchain execution.

The local simulator is included because it can be executed safely by reviewers immediately. The SDK file shows how the same flow maps to the live Subscriptions program.

## Why This Use Case Fits the Primitive

The normal SPL Token delegate model allows one delegate per token account. Solana Subscriptions & Allowances adds a Subscription Authority PDA that can support multiple policy-controlled delegations at once.

For agentic commerce, that means a user can approve:

- which agent may spend;
- which mint/token account is involved;
- how much can be spent;
- when the authorization expires;
- whether the budget is fixed or recurring.

The agent gets autonomy. The user keeps a hard cap.

## Files

```text
solana-subscriptions-code-sample/
├── README.md
├── package.json
├── src/
│   ├── local-simulator.js
│   └── sdk-flow.ts
└── test/
    └── local-simulator.test.js
```

## Run the Local Demo

```bash
npm test
npm run demo
```

Expected behavior:

- creates a weekly allowance;
- performs two valid pulls;
- rejects a pull that would exceed the remaining cap;
- revokes the allowance;
- rejects any pull after revocation.

No Solana wallet, private key, RPC endpoint, KYC, phone number, or token balance is required for this local demonstration.

## Example Output

```text
created allowance: 20000000 units for agent-coder-1
pull ok: pay.sh api-search 3500000
pull ok: rpc-provider indexing 9000000
blocked: allowance exceeded
revoked allowance
blocked: allowance revoked
remaining allowance: 7500000
```

The unit convention in the sample is `USDC * 1_000_000`, so `20_000_000` equals 20 USDC.

## Onchain Mapping

The local model maps to the official program as follows:

| Local simulator concept | Solana Subscriptions concept |
|---|---|
| `AllowanceBook.createFixedAllowance()` | `initSubscriptionAuthority` + `createFixedDelegation` |
| `pull()` | `transferFixed` |
| `remainingUnits` | fixed delegation account remaining `amount` |
| `revoked` | `revokeDelegation` |
| `agentId` | delegatee public key |
| `ownerId` | delegator public key |

For a weekly budget that resets every period, use `createRecurringDelegation` and `transferRecurring` instead of fixed delegation.

## Official SDK Pattern

The `src/sdk-flow.ts` file follows the public SDK README pattern:

```typescript
await client.subscriptions.instructions.initSubscriptionAuthority({
  owner,
  tokenMint,
  userAta,
  tokenProgram,
});

await client.subscriptions.instructions.createFixedDelegation({
  delegator,
  tokenMint,
  delegatee,
  nonce,
  amount,
  expiryTs,
});
```

It intentionally does not include a private key or hard-coded wallet. Reviewers can wire their own signer, mint, ATA, and RPC endpoint.

## Security Notes

- The demo never stores or asks for a private key.
- It does not connect a wallet.
- It does not make token transfers.
- It models the authorization rules locally, then points to the official SDK flow for real execution.
- In a production app, wallet UI must explain the Subscription Authority PDA and show all active delegations, caps, expiry dates, and revoke actions.

## Sources

- Solana announcement: https://solana.com/news/subscriptions-and-allowances
- Official repository: https://github.com/solana-program/subscriptions
- TypeScript SDK README: https://github.com/solana-program/subscriptions/tree/main/clients/typescript
- Subscription plan docs: https://solana.com/docs/payments/subscriptions/subscription-plan
