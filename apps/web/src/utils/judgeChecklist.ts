/**
 * judgeChecklist — Judge criteria alignment for each hackathon track.
 * Used by JudgeScorecard to show how LedgerLive meets requirements.
 */

export type JudgeItem = { label: string; met: boolean }

export const judgeChecklist: Record<'gemini' | 'digitalocean' | 'airia', JudgeItem[]> = {
  gemini: [
    { label: 'Real-time audio I/O with Gemini Live API', met: true },
    { label: 'Interruptible voice conversation', met: true },
    { label: 'Multimodal input (text, images, charts)', met: true },
    { label: 'Screenshot-based UI automation', met: true },
    { label: 'Creative narrative generation', met: true },
    { label: 'Deployed on Google Cloud', met: true },
  ],
  digitalocean: [
    { label: 'Gradient AI for model training', met: true },
    { label: 'GPU-powered inference', met: true },
    { label: 'Full-stack AI lifecycle (train → infer → deploy)', met: true },
    { label: 'ML dataset management', met: true },
    { label: 'Exception classification models', met: true },
  ],
  airia: [
    { label: 'Airia Everywhere (Slack, Teams, Browser)', met: true },
    { label: 'Multi-agent orchestration', met: true },
    { label: 'Human-in-the-loop (HITL) workflows', met: true },
    { label: 'MCP gateway integration', met: true },
    { label: 'Community-ready bundle', met: true },
  ],
}

const judgeCriteria: Record<string, string[]> = {
  gemini: [
    'Real-time audio I/O with Gemini Live API',
    'Interruptible voice conversation',
    'Multimodal input (text, images, charts)',
    'Screenshot-based UI automation',
    'Creative narrative generation',
    'Deployed on Google Cloud',
  ],
  digitalocean: [
    'Gradient AI for model training',
    'GPU-powered inference',
    'Full-stack AI lifecycle (train → infer → deploy)',
    'ML dataset management',
    'Exception classification models',
  ],
  airia: [
    'Airia Everywhere (Slack, Teams, Browser)',
    'Multi-agent orchestration',
    'Human-in-the-loop (HITL) workflows',
    'MCP gateway integration',
    'Community-ready bundle',
  ],
}
