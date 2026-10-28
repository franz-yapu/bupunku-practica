import { Inject, Injectable } from "@angular/core";
import { environment } from "../../../environments/environment";
import { map, Observable } from "rxjs";
import { HttpClient, HttpParams } from "@angular/common/http";

import { RespuestaBusqueda, Libro } from "../../interfaces/libro.interface";




@Injectable({
    providedIn: 'root'
})
export class LibrosService {
    private readonly http = Inject(HttpClient);
    private readonly baseUrl: string = 'https://openlibrary.org/search.json';

    buscar(texto: string): Observable<Libro[]> {
    const params = new HttpParams().set('q', texto).set('limit', 10);

    return this.http.get<RespuestaBusqueda>(this.baseUrl, { params })
    .pipe(
      map((respuesta: RespuestaBusqueda) =>
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

