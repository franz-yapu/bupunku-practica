import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';

import { Libro, RespuestaBusqueda } from './libro.model';

@Injectable({ providedIn: 'root' })
export class LibrosService {
  private readonly http = inject(HttpClient);
  private readonly url = 'https://openlibrary.org/search.json';

  buscar(texto: string): Observable<Libro[]> {
    const params = new HttpParams().set('q', texto).set('limit', 10);

    return this.http.get<RespuestaBusqueda>(this.url, { params }).pipe(
      map((respuesta) =>
        respuesta.docs.map((doc) => ({
          id: doc.key,
          titulo: doc.title,
          autores: doc.author_name ?? [],
          anio: doc.first_publish_year ?? null,
        })),
      ),
    );
  }
}
