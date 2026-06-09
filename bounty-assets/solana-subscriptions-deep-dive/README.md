# Solana Subscriptions & Allowances: A Builder's Deep Dive

Submission for Superteam Canada bounty:
https://superteam.fun/earn/listing/publish-technical-deep-dive-on-solana-subscriptions-and-allowances-primitive

Author: Brandon Bounty
Last checked: June 9, 2026

## Executive Summary

Solana Subscriptions & Allowances turns recurring payments and delegated spending into shared onchain infrastructure. Instead of every SaaS app, API provider, agent platform, or payroll tool building a custom billing contract and audit surface, Solana now has a standard program for three related flows:

- fixed allowances, where a user delegates a capped one-time budget;
- recurring delegations, where a delegate can pull up to a cap each period;
- subscription plans, where a merchant publishes billing terms and subscribers opt in.

The important architectural move is the Subscription Authority PDA. SPL Token accounts normally support only one delegate at a time. That works for a single approval, but it does not work if a user wants to subscribe to multiple services, give an AI agent a spending budget, and authorize a card-linked program from the same token account. The subscriptions program solves that by making one per-user/per-mint PDA the token account's delegate, then enforcing the real policy in separate delegation PDAs.

The result is not just "Stripe, but on Solana." It is a lower-level primitive for pull-based value flows. That matters for API billing, agentic commerce, payroll, media micropayments, stablecoin invoicing, and any product where the user should approve spending rules once instead of signing every payment manually.

## What Shipped

The Solana Foundation announced Subscriptions & Allowances on June 2, 2026. The program is open source, live on mainnet, and designed as shared infrastructure for recurring billing and delegated spending. The official announcement describes it as one audited program that teams can integrate instead of building custom recurring-payment infrastructure.

The public repository is `solana-foundation/subscriptions`. The README describes the program as a Solana program and client set for managed token delegations across SPL Token and Token-2022. It also publishes the program ID:

```text
De1egAFMkMWZSN5rYXRj9CAdheBamobVNubTsi9avR44
```

The repository includes:

- the Rust Solana program;
- generated TypeScript and Rust clients;
- docs and runbooks;
- a demo web app;
- integration tests and benchmarking.

For builders, the TypeScript client is the practical starting point. The official docs install it with:

```bash
pnpm add @solana/subscriptions @solana/kit @solana/kit-plugin-rpc @solana/kit-plugin-signer @solana-program/token
```

## The Core Problem: One Token Account, One Delegate

The normal SPL Token delegate model is simple: a token owner approves a delegate, and that delegate can transfer up to the approved amount. This is useful, but it has a structural constraint: a token account can only have one active delegate.

That means the raw model does not compose well.

Imagine a user has one USDC token account and wants to authorize:

- a $20/month newsletter subscription;
- a $49/month developer API plan;
- a $100 weekly budget for an AI agent;
- a card-linked spending program;
- a contractor payout every two weeks.

If each product independently sets itself as the token delegate, each new approval overwrites the previous one. The user does not get a portfolio of spending rules. They get one fragile delegate slot.

Subscriptions & Allowances fixes this with a policy layer.

## The Subscription Authority PDA

For each `(user, mint)` pair, the program derives a Subscription Authority PDA. Conceptually:

```text
SubscriptionAuthority = PDA("SubscriptionAuthority", user_pubkey, mint_pubkey)
```

The user initializes this authority and approves it as the token account's single delegate with a maximum allowance. From SPL Token's point of view, the one-delegate rule is still respected. There is only one delegate: the Subscription Authority.

But the Subscription Authority does not mean "anyone can spend everything." The Subscription Authority can only move funds when the subscriptions program finds a valid delegation PDA or subscription PDA authorizing that exact pull.

The pattern is:

```text
SPL Token account
  -> single delegate: Subscription Authority PDA
       -> fixed delegation PDA
       -> recurring delegation PDA
       -> subscription plan subscriber PDA
       -> more policy PDAs
```

The Subscription Authority is the router. The delegation PDAs are the rules.

That distinction matters. The broad SPL approval is not the product policy. It is the mechanical permission needed to let the program enforce many smaller policies. Each actual transfer must still pass checks for amount, period, expiry, destination, plan terms, and authority.

## The Three Models

### 1. Fixed Delegation

Fixed delegation is best understood as an allowance.

A user authorizes a delegate to spend up to a total amount. The delegation can optionally expire. Each pull reduces the remaining cap until it is exhausted.

Good fits:

- AI agent budget: "This agent can spend up to 25 USDC before Friday."
- One-off service usage: "This CLI can buy up to 10 API calls."
- Controlled trial: "This app can pull up to 5 USDC during onboarding."

The safety property is straightforward: the delegate gets autonomy, but only inside a bounded budget.

### 2. Recurring Delegation

Recurring delegation is a repeating allowance.

The user authorizes a delegate to pull up to a cap each period. The cap resets on cadence. Missed periods do not need to accumulate into an unlimited claim; the delegation is still bounded by the program's accounting rules.

Good fits:

- payroll or contractor payouts;
- recurring grants;
- family or team spending allowances;
- treasury operations with periodic limits.

This model is user-defined. It is less like a merchant plan and more like a payer saying, "This recipient can pull this much every period."

### 3. Subscription Plans

Subscription plans flip the direction. The merchant publishes billing terms onchain, and users subscribe to those terms.

The official docs describe the flow as:

1. merchant creates a plan;
2. subscriber accepts the plan;
3. merchant or approved puller collects from the subscription PDA.

The plan has pricing terms such as amount and period. Existing subscribers keep the terms they accepted. If a merchant wants to change pricing for future subscribers, the clean model is to publish updated plan terms for new subscriptions rather than silently changing what existing subscribers accepted.

Good fits:

- API tiers;
- SaaS subscriptions;
- stablecoin invoice collection;
- paid content memberships;
- infrastructure provider billing.

## Why This Matters for Agentic Commerce

Autonomous agents need spending autonomy, but users need caps.

Without a primitive like this, agentic commerce has an awkward UX:

- the agent asks the user to sign every payment;
- the user gives the agent custody, which is too risky;
- the app runs billing offchain and reintroduces a centralized payment processor;
- each provider builds custom escrow or subscription logic.

Subscriptions & Allowances gives a better middle path.

A user can authorize a bounded allowance. The agent can then pay for APIs, storage, models, data sources, or actions without interrupting the user every time. The user still controls:

- which token account and mint are involved;
- who can pull;
- how much can be pulled;
- when the authorization expires;
- whether the arrangement is fixed, recurring, or plan-based.

That is a useful primitive for pay.sh. Pay.sh is framed as a pay-as-you-go API payment layer for APIs and agentic commerce. With allowances, an agent can discover and pay for endpoints while staying inside a user-approved budget. With subscription plans, API providers can offer flat-fee recurring access.

## Tradeoffs and Design Constraints

### Better Composability, More Program Trust

The design improves composability because many delegations can coexist behind one Subscription Authority. The tradeoff is that users and integrators now rely on the subscriptions program as the policy engine.

That is why the program being open source, audited, and standard matters. If every merchant ships its own custom recurring billing program, users face fragmented security assumptions. A shared primitive concentrates review and improves wallet UX.

### Broad Delegate Approval Looks Scary Unless Wallets Explain It

The Subscription Authority uses a broad SPL approval internally. To a naive wallet UI, that can look risky. The correct user-facing explanation is not "approve unlimited spending to a merchant." It is "enable a standard Subscription Authority for this token, then approve specific capped arrangements."

Wallets need to show the policy layer clearly:

- active delegations;
- per-period or total cap;
- expiry;
- puller;
- next eligible collection;
- revoke/cancel action.

The primitive is strong, but wallet UX will determine whether users trust it.

### Plan Terms Need Good Indexing

Subscription plans are onchain, but products need readable dashboards. Builders should index:

- plan creation;
- subscription creation;
- cancellations;
- successful pulls;
- failed pulls;
- remaining allowance;
- next billing window.

The repository notes that the program emits onchain events via self-CPI for indexer integration. That is important because recurring payments are operational workflows, not just one-off transfers.

### Token-2022 Support Is Powerful but Needs Care

Support for SPL Token and Token-2022 expands the design space. Token-2022 features can enable stablecoin and enterprise use cases, but token extensions can also change transfer behavior. Integrators should verify mint compatibility rather than assuming every mint is safe for delegated pulls.

## Practical Integration Architecture

A production integration should separate the onchain primitive from application workflow.

### Merchant Side

For a subscription plan:

1. choose mint and denomination;
2. create metadata describing the plan;
3. create the plan onchain;
4. expose the plan in the app UI;
5. index subscribers and pull events;
6. run a collection service or approved puller.

### User Side

For a subscriber:

1. initialize Subscription Authority for the mint if needed;
2. review plan amount, period, merchant, and pullers;
3. subscribe;
4. monitor active subscriptions;
5. cancel or revoke when needed.

### Agent Side

For an AI agent allowance:

1. user approves a fixed or recurring delegation;
2. agent receives only enough context to know its budget and expiry;
3. agent pays providers through allowed pull flows;
4. app monitors remaining budget and failed pulls;
5. user can revoke when the task ends.

## Canadian Relevance

The bounty asks for Canadian relevance, so here are concrete Canadian business contexts where this primitive is useful.

### Shopify: Merchant App Billing and Stablecoin Checkout

Shopify's app ecosystem depends on recurring billing, usage-based billing, and merchant subscriptions. A Solana-native subscription primitive could support crypto-native merchant tools that bill in stablecoins while keeping billing terms visible and revocable onchain.

This is not a claim that Shopify is integrating the primitive today. It is a fit analysis: Shopify-style merchant tooling is exactly the kind of recurring SaaS workflow the primitive targets.

### Wealthsimple: Controlled Stablecoin Allowances

Wealthsimple operates in consumer finance, where user consent, revocation, and clear spending limits matter. A future stablecoin product could use recurring delegations for user-authorized transfers, automated contributions, or controlled subscription payments without handing custody to a third party.

The key benefit would be user-readable financial permissions instead of opaque card rails.

### Dapper Labs: Consumer Apps and NFT/Media Subscriptions

Dapper Labs has experience bringing mainstream users into crypto consumer products. Subscriptions & Allowances could support recurring fan memberships, content access, marketplace tools, or creator subscriptions where users approve stablecoin pulls with clear caps.

The broader lesson for Canadian builders is that recurring crypto UX does not need to be a custom contract every time.

## What I Would Build First

The highest-leverage demo is an "agent API allowance manager."

User story:

> A developer gives an AI coding agent a 20 USDC weekly budget. The agent can spend that budget on pay.sh API calls, RPC credits, model endpoints, or data providers. The user sees every pull and can revoke the allowance instantly.

Why this demo is strong:

- It uses the fixed or recurring delegation model naturally.
- It connects directly to pay.sh and agentic commerce.
- It avoids pretending the product is only for SaaS subscriptions.
- It makes the safety benefit visible: autonomy with a cap.

Core screens:

- Create allowance: token, delegate, cap, expiry/cadence.
- Active allowances: remaining amount, expiry, revoke.
- Agent activity: provider, amount, timestamp, reason.
- Pull failure states: insufficient funds, expired delegation, cap exceeded.

Technical shape:

- TypeScript client with `@solana/subscriptions`.
- Devnet mint for demo.
- One delegate wallet representing the agent.
- A simple local service that attempts pulls and records outcomes.
- README explaining every PDA and transfer path.

## Builder Checklist

Before shipping against this primitive, I would verify:

- Does the target mint work with the program's extension checks?
- Does the wallet explain Subscription Authority clearly?
- Can users revoke one delegation without breaking unrelated subscriptions?
- Are plan terms displayed before signing?
- Are existing subscribers protected from unexpected plan changes?
- Are pullers scoped and auditable?
- Is there an indexer for failed and successful pulls?
- Are grace periods and failed billing retries handled at the app layer?
- Is the UI explicit about whether a flow is fixed, recurring, or merchant-plan based?

## Conclusion

Solana Subscriptions & Allowances is important because it moves recurring billing and delegated spending from custom app logic into a shared primitive.

The architecture is clean:

- one Subscription Authority PDA per `(user, mint)`;
- one broad token delegate at the SPL layer;
- many policy-controlled delegation PDAs at the subscriptions layer;
- three models for fixed budgets, recurring budgets, and merchant plans.

The near-term opportunity is not only SaaS subscriptions. It is agentic commerce with bounded budgets. That is where allowances become more than a billing primitive: they become a trust primitive for autonomous software.

For developers, the next step is to build demos that make the policy layer obvious. Users should understand what can be pulled, by whom, how often, and how to revoke it. If wallets and apps get that right, this primitive can make stablecoin subscriptions and agent spending feel native instead of bolted on.

## Sources

- Solana Foundation announcement: https://solana.com/news/subscriptions-and-allowances
- Solana subscriptions repository: https://github.com/solana-program/subscriptions
- Official subscription plan docs: https://solana.com/docs/payments/subscriptions/subscription-plan
- Chainstack technical walkthrough: https://docs.chainstack.com/docs/solana-subscriptions-and-allowances
