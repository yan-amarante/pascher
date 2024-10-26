// src/app/services/sse.service.ts
import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SseService {

  constructor(private zone: NgZone) {}

  getServerSentEvents(url: string): Observable<string> {
    return new Observable<string>((observer) => {
      const eventSource = new EventSource(url);

      eventSource.onmessage = (event) => {
        // Run inside Angular's zone to ensure updates propagate correctly
        this.zone.run(() => observer.next(event.data));
      };

      eventSource.onerror = (error) => {
        console.error('SSE error:', error);  
        // Retry connection on error after a delay
        setTimeout(() => this.getServerSentEvents(url), 5000);
      };

      return () => eventSource.close();
    });
  }
}
