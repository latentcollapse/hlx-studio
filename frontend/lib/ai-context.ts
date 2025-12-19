/**
 * AI Context - Backend status and management
 * Provides status information for Helix 5.1B Brain
 */

import { helixBrain } from '../services/helixBrain';

export interface AIBackendStatus {
  isHealthy: boolean;
  provider: string;
  model: string;
  gpu_available: boolean;
  gpu_memory?: {
    allocated_gb: number;
    reserved_gb: number;
    total_gb: number;
    free_gb: number;
  };
}

/**
 * Get AI backend status
 */
export async function getAIBackendStatus(): Promise<AIBackendStatus> {
  const status = await helixBrain.getStatus();

  if (!status) {
    return {
      isHealthy: false,
      provider: 'Helix Brain',
      model: 'Helix 5.1B MoE (unavailable)',
      gpu_available: false,
    };
  }

  return {
    isHealthy: status.ready,
    provider: 'Helix Brain',
    model: 'Helix 5.1B MoE',
    gpu_available: status.gpu_available,
    gpu_memory: status.gpu_memory || undefined,
  };
}

/**
 * Reload models (e.g., after training completes)
 */
export async function reloadAIBackend(): Promise<boolean> {
  const result = await helixBrain.reload();
  return result.success;
}
