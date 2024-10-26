// src/app/components/selenium-output/selenium-output.component.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { SseService } from '../../services/sse.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-selenium-output',
  template: `
    <h2>Script Output</h2>
    <div *ngFor="let message of messages">
      {{ message }}
    </div>
  `,
  standalone: true,
  imports: [CommonModule]  // Import CommonModule here
})
export class SeleniumOutputComponent implements OnInit, OnDestroy {
  messages: string[] = [];
  private sseSubscription: any;

  constructor(private sseService: SseService) {}

  ngOnInit(): void {
    // Subscribe to the SSE from the backend endpoint
    this.sseSubscription = this.sseService.getServerSentEvents('http://localhost:8080/run-selenium-script')
      .subscribe({
        next: (message) => this.messages.push(message),
        error: (error) => console.error('SSE error:', error)
      });
  }

  ngOnDestroy(): void {
    // Unsubscribe to avoid memory leaks
    if (this.sseSubscription) {
      this.sseSubscription.unsubscribe();
    }
  }
}
