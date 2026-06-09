import { address, createClient, type Address, type TransactionSigner } from "@solana/kit";
import { solanaLocalRpc } from "@solana/kit-plugin-rpc";
import { signer } from "@solana/kit-plugin-signer";
import {
  findFixedDelegationPda,
  findSubscriptionAuthorityPda,
  subscriptionsProgram,
} from "@solana/subscriptions";

export const SUBSCRIPTIONS_PROGRAM_ID = address(
  "De1egAFMkMWZSN5rYXRj9CAdheBamobVNubTsi9avR44",
);

export type AgentAllowanceConfig = {
  owner: TransactionSigner;
  ownerAta: Address;
  agentDelegatee: Address;
  tokenMint: Address;
  tokenProgram: Address;
  nonce: bigint;
  amountUnits: bigint;
  expiryTs: bigint;
  rpcUrl?: string;
};

export async function createAgentFixedAllowance(config: AgentAllowanceConfig) {
  const client = createClient()
    .use(signer(config.owner))
    .use(solanaLocalRpc({ rpcUrl: config.rpcUrl ?? "http://127.0.0.1:8899" }))
    .use(subscriptionsProgram());

  const initAuthorityIx = await client.subscriptions.instructions.initSubscriptionAuthority({
    owner: config.owner,
    tokenMint: config.tokenMint,
    userAta: config.ownerAta,
    tokenProgram: config.tokenProgram,
  });

  const createDelegationIx = await client.subscriptions.instructions.createFixedDelegation({
    delegator: config.owner,
    tokenMint: config.tokenMint,
    delegatee: config.agentDelegatee,
    nonce: config.nonce,
    amount: config.amountUnits,
    expiryTs: config.expiryTs,
  });

  const [subscriptionAuthorityPda] = await findSubscriptionAuthorityPda({
    user: config.owner.address,
    tokenMint: config.tokenMint,
  });

  const [fixedDelegationPda] = await findFixedDelegationPda({
    subscriptionAuthority: subscriptionAuthorityPda,
    delegator: config.owner.address,
    delegatee: config.agentDelegatee,
    nonce: config.nonce,
  });

  return {
    instructions: [initAuthorityIx, createDelegationIx],
    subscriptionAuthorityPda,
    fixedDelegationPda,
  };
}

export type AgentPullConfig = {
  delegatee: TransactionSigner;
  delegator: Address;
  delegatorAta: Address;
  receiverAta: Address;
  tokenMint: Address;
  tokenProgram: Address;
  fixedDelegationPda: Address;
  amountUnits: bigint;
  rpcUrl?: string;
};

export async function transferFromAgentAllowance(config: AgentPullConfig) {
  const client = createClient()
    .use(signer(config.delegatee))
    .use(solanaLocalRpc({ rpcUrl: config.rpcUrl ?? "http://127.0.0.1:8899" }))
    .use(subscriptionsProgram());

  return client.subscriptions.instructions.transferFixed({
    delegatee: config.delegatee,
    delegator: config.delegator,
    delegatorAta: config.delegatorAta,
    tokenMint: config.tokenMint,
    delegationPda: config.fixedDelegationPda,
    amount: config.amountUnits,
    receiverAta: config.receiverAta,
    tokenProgram: config.tokenProgram,
  });
}
