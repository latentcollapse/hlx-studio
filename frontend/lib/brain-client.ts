/**
 * Brain Client - Wrapper for Helix 5.1B Brain Service
 * Provides backward-compatible interface for existing HelixCLI
 */

import { helixBrain, HelixQueryResponse } from '../services/helixBrain';

export interface BrainStatus {
  isHealthy: boolean;
  modelName: string;
  version: string;
  specialists: {
    coordinator: string;
    ascii: string;
    runic: string;
  };
}

export interface AskBrainParams {
  question: string;
  use_rag?: boolean;
  temperature?: number;
}

/**
 * Ask the Helix brain a question
 */
export async function askBrain(params: AskBrainParams): Promise<string> {
  const response: HelixQueryResponse = await helixBrain.query(params.question);

  if (!response.success) {
    throw new Error(response.error || 'Brain query failed');
  }

  // Format response with specialist info if available
  let formattedResponse = response.response;

  if (response.explanation) {
    formattedResponse = `${response.explanation}\n\n${response.response}`;
  }

  if (response.format_hints && response.format_hints.length > 0) {
    formattedResponse += `\n\n💡 Formats detected: ${response.format_hints.join(', ')}`;
  }

  return formattedResponse;
}

/**
 * Get brain status
 */
export async function getBrainStatus(): Promise<BrainStatus> {
  const status = await helixBrain.getStatus();

  if (!status) {
    return {
      isHealthy: false,
      modelName: 'Helix 5.1B (unavailable)',
      version: '5.1.0',
      specialists: {
        coordinator: 'unavailable',
        ascii: 'unavailable',
        runic: 'unavailable',
      },
    };
  }

  return {
    isHealthy: status.ready,
    modelName: 'Helix 5.1B MoE',
    version: '5.1.0',
    specialists: status.models,
  };
}
