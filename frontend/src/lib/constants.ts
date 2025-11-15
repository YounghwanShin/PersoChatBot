export const SAMPLE_QUESTIONS = [
  'Perso.ai는 어떤 서비스인가요?',
  'Perso.ai의 주요 기능은 무엇인가요?',
  'Perso.ai는 어떤 기술을 사용하나요?',
  'Perso.ai의 사용자는 어느 정도인가요?',
  'Perso.ai에서 지원하는 언어는 몇 개인가요?',
  'Perso.ai의 요금제는 어떻게 구성되어 있나요?',
] as const;

export const MAX_CONVERSATION_HISTORY = 5;

export const ERROR_MESSAGES = {
  DEFAULT: '죄송합니다. 응답을 생성하는 중 오류가 발생했습니다.',
  SERVER_ERROR: '서버에 일시적인 문제가 발생했습니다. 잠시 후 다시 시도해주세요.',
  RATE_LIMIT: '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.',
  LOADING: '답변을 생성하고 있습니다...',
} as const;
