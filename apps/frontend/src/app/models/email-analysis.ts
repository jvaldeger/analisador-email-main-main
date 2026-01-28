export interface EmailAnalysis {
  category: string;
  confidence: number;
  suggested_response: string;
  original_text_preview: string;
}

export interface ClassificationRequest {
  email_text?: string;
  file?: File;
}