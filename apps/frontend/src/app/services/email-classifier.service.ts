import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { EmailAnalysis } from '../models/email-analysis';





@Injectable({
  providedIn: 'root'
})
export class EmailClassifierService {
  private apiUrl = 'https://analisador-email-backend.vercel.app/api/classify';
  

  constructor(private http: HttpClient) { }

  classifyEmailByText(emailText: string): Observable<EmailAnalysis> {
    const formData = new FormData();
    formData.append('email_text', emailText);
    return this.http.post<EmailAnalysis>(this.apiUrl, formData);
  }

  classifyEmailByFile(file: File): Observable<EmailAnalysis> {
    const formData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post<EmailAnalysis>(this.apiUrl, formData);
  }

}

