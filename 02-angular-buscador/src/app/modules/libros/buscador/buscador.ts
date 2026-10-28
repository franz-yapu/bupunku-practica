import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { LibrosService } from '../libros.service';
import { debounceTime, distinctUntilChanged, filter, map, switchMap } from 'rxjs';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-buscador',
  styleUrl: './buscador.css',
  templateUrl: './buscador.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Buscador {
  constructor() {
  this.searchTerm.valueChanges
    .pipe(
      map((texto) => texto.trim()),
      debounceTime(300),
      distinctUntilChanged(),
      filter((texto) => texto.length >= 3),
      switchMap((texto) => this.librosService.buscar(texto)),
    )
    .subscribe((libros) => console.log(libros));
}

  private readonly librosService = inject(LibrosService); 

  readonly searchTerm = new FormControl('', { nonNullable: true });
}
