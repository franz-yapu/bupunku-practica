import { Component } from '@angular/core';
import { Buscador } from './libros/buscador';

@Component({
  selector: 'app-root',
  imports: [Buscador],
  template: `<app-buscador />`,
})
export class App {}
