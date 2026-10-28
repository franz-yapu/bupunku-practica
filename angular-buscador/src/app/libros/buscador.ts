import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { catchError, debounceTime, distinctUntilChanged, filter, map, of, switchMap, tap } from 'rxjs';

import { Libro } from './libro.model';
import { LibrosService } from './libros.service';

@Component({
  selector: 'app-buscador',
  imports: [ReactiveFormsModule],
  templateUrl: './buscador.html',
  styleUrl: './buscador.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Buscador {
  private readonly librosService = inject(LibrosService);

  readonly busqueda = new FormControl('', { nonNullable: true });

  readonly libros = signal<Libro[]>([]);
  readonly cargando = signal(false);
  readonly error = signal<string | null>(null);
  readonly total = computed(() => this.libros().length);

  constructor() {
    this.busqueda.valueChanges
      .pipe(
        map((texto) => texto.trim()),
        debounceTime(300),
        distinctUntilChanged(),
        filter((texto) => texto.length >= 3),
        tap(() => {
          this.cargando.set(true);
          this.error.set(null);
        }),
        switchMap((texto) =>
          this.librosService.buscar(texto).pipe(
            catchError(() => {
              this.error.set('No se pudo conectar. Revisa tu conexión e intenta de nuevo.');
              return of([]);
            }),
          ),
        ),
        takeUntilDestroyed(),
      )
      .subscribe((libros) => {
        this.libros.set(libros);
        this.cargando.set(false);
      });
  }
}
