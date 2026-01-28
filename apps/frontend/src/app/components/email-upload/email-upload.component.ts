import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FileSizePipe } from '../../pipes/file-size.pipe';


@Component({
  selector: 'app-email-upload',
  standalone: true,
  imports: [CommonModule, FormsModule, FileSizePipe], // ← ADICIONE FileSizePipe AQUI
  templateUrl: './email-upload.component.html',
  styleUrl: './email-upload.component.css'
})
export class EmailUploadComponent {
  @Output() textSubmit = new EventEmitter<string>();
  @Output() fileSubmit = new EventEmitter<File>();

  emailText = '';
  selectedFile: File | null = null;
  isDragging = false;
  acceptedTypes = '.txt,.pdf';

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      if (this.isValidFileType(file)) {
        this.selectedFile = file;
      } else {
        alert('Tipo de arquivo inválido. Use apenas .txt ou .pdf');
        this.selectedFile = null;
      }
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragging = false;
    
    if (event.dataTransfer?.files) {
      const file = event.dataTransfer.files[0];
      if (this.isValidFileType(file)) {
        this.selectedFile = file;
      } else {
        alert('Tipo de arquivo inválido. Use apenas .txt ou .pdf');
      }
    }
  }

  isValidFileType(file: File): boolean {
    const allowedTypes = ['text/plain', 'application/pdf'];
    const allowedExtensions = ['.txt', '.pdf'];
    
    // Verifica pelo tipo MIME
    if (allowedTypes.includes(file.type)) {
      return true;
    }
    
    // Verifica pela extensão do arquivo
    const fileName = file.name.toLowerCase();
    return allowedExtensions.some(ext => fileName.endsWith(ext));
  }

  submitText(): void {
    if (this.emailText.trim()) {
      this.textSubmit.emit(this.emailText);
    }
  }

  submitFile(): void {
    if (this.selectedFile) {
      this.fileSubmit.emit(this.selectedFile);
    }
  }

  clearForm(): void {
    this.emailText = '';
    this.selectedFile = null;
  }

  formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
}