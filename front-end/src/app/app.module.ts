// src/app/app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { SeleniumOutputComponent } from './components/selenium-output/selenium-output.component';
import { SseService } from './services/sse.service';

@NgModule({
  declarations: [
    AppComponent,
    SeleniumOutputComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [SseService],
  bootstrap: [AppComponent]
})
export class AppModule { }
