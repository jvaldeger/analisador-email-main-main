import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EmailUploadComponent } from './components/email-upload/email-upload.component';
import { ResultDisplayComponent } from './components/result-display/result-display.component';
import { LoadingSpinnerComponent } from './components/loading-spinner/loading-spinner.component';
import { EmailClassifierService } from './services/email-classifier.service';
import { EmailAnalysis } from './models/email-analysis';
import { Observable } from 'rxjs';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, EmailUploadComponent, ResultDisplayComponent, LoadingSpinnerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Email Analyzer';
  analysis: EmailAnalysis | null = null;
  loading = false;
  error: string | null = null;

  constructor(private emailService: EmailClassifierService, private cdr: ChangeDetectorRef) {}

  onTextSubmit(text: string): void {
    this.analyzeEmail(() => this.emailService.classifyEmailByText(text)).then(analysis => {
      this.analysis = analysis;
      this.cdr.detectChanges(); 

    });
  }

  onFileSubmit(file: File): void {
    this.analyzeEmail(() => this.emailService.classifyEmailByFile(file)).then(analysis => {
      this.analysis = analysis;
      this.cdr.detectChanges(); 

    });
  }



  private async analyzeEmail(apiCall: () => Observable<EmailAnalysis>): Promise<EmailAnalysis | null> {
    this.loading = true;
    this.error = null;
    this.analysis = null;

    return new Promise((resolve, reject) => {
      apiCall().subscribe({
        next: (response: EmailAnalysis) => {
          this.analysis = response;
          this.loading = false;
          console.log('Resposta:', response);
          resolve(response); 
        },
        error: (error: any) => {
          this.error = error?.message || 'An error occurred';
          this.loading = false;
          console.error('Erro:', error);
          resolve(null); 
        }
      });
    });
  }


  clearResults(): void {
    this.analysis = null;
    this.error = null;
  }
}
