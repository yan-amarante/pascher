import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SeleniumOutputComponent } from './components/selenium-output/selenium-output.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SeleniumOutputComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'pascher';
}
