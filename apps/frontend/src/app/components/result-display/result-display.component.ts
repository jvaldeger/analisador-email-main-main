import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EmailAnalysis } from '../../models/email-analysis';



@Component({
  selector: 'app-result-display',
  standalone: true,
  imports: [CommonModule],
templateUrl: './result-display.component.html',
styleUrl: './result-display.component.css',

})
export class ResultDisplayComponent {
  @Input() analysis: EmailAnalysis | null = null;
  @Input() loading = false;
  @Input() error: string | null = null;

  get categoryClass(): string {
    if (!this.analysis) return '';
    return this.analysis.category === 'Produtivo' ? 'category-productive' : 'category-unproductive';
  }

  get confidenceColor(): string {
    if (!this.analysis) return '#95a5a6';
    const confidence = this.analysis.confidence * 100;
    if (confidence >= 80) return '#2ecc71';
    if (confidence >= 60) return '#f39c12';
    return '#e74c3c';
  }

  copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(() => {
      // Você pode adicionar um toast/notification aqui
      console.log('Texto copiado para a área de transferência');
    });
  }
}