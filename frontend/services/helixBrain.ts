/**
 * Helix 5.1B Brain Service Client
 *
 * Communicates with the Helix 5.1B MoE backend service.
 * Provides a conversational AI interface for HLX operations.
 */

export interface HelixQueryRequest {
  query: string;
}

export interface HelixQueryResponse {
  success: boolean;
  response: string;
  specialist: 'coordinator' | 'ascii' | 'runic';
  explanation?: string;
  format_hints?: string[];
  coordinator_reasoning?: string;
  error?: string;
  details?: string;
}

export interface HelixHealthResponse {
  status: 'ready' | 'loading';
  models: {
    coordinator: string;
    ascii: string;
    runic: string;
  };
  greeting: string;
}

export interface HelixStatusResponse {
  ready: boolean;
  models: {
    coordinator: string;
    ascii: string;
    runic: string;
  };
  coordinator: string;
  ascii_specialist: string;
  runic_specialist: string;
  gpu_available: boolean;
  gpu_memory?: {
    allocated_gb: number;
    reserved_gb: number;
    total_gb: number;
    free_gb: number;
  };
}

class HelixBrainClient {
  private baseUrl: string;
  private isReady: boolean = false;

  constructor(baseUrl: string = 'http://localhost:5001') {
    this.baseUrl = baseUrl;
    this.checkHealth();
  }

  /**
   * Check if the brain service is ready
   */
  async checkHealth(): Promise<HelixHealthResponse | null> {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      const data = await response.json();
      this.isReady = data.status === 'ready';
      return data;
    } catch (error) {
      console.error('Helix brain not available:', error);
      this.isReady = false;
      return null;
    }
  }

  /**
   * Get detailed status of the brain service
   */
  async getStatus(): Promise<HelixStatusResponse | null> {
    try {
      const response = await fetch(`${this.baseUrl}/status`);
      return await response.json();
    } catch (error) {
      console.error('Failed to get status:', error);
      return null;
    }
  }

  /**
   * Send a query to the Helix brain
   */
  async query(text: string): Promise<HelixQueryResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: text }),
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          response: '',
          specialist: 'coordinator',
          error: data.error || 'Unknown error',
          details: data.details,
        };
      }

      return data;
    } catch (error) {
      return {
        success: false,
        response: '',
        specialist: 'coordinator',
        error: 'Failed to connect to Helix brain',
        details: error instanceof Error ? error.message : String(error),
      };
    }
  }

  /**
   * Reload models (useful after training completes)
   */
  async reload(): Promise<{ success: boolean; message?: string; error?: string }> {
    try {
      const response = await fetch(`${this.baseUrl}/reload`, {
        method: 'POST',
      });
      return await response.json();
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error),
      };
    }
  }

  /**
   * Check if the service is ready
   */
  get ready(): boolean {
    return this.isReady;
  }

  /**
   * Wait for the service to be ready
   */
  async waitForReady(timeoutMs: number = 30000): Promise<boolean> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeoutMs) {
      const health = await this.checkHealth();
      if (health && health.status === 'ready') {
        return true;
      }
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    return false;
  }
}

// Singleton instance
export const helixBrain = new HelixBrainClient();

// Export class for testing
export { HelixBrainClient };
