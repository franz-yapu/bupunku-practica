import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { Libro } from './libro.model';
import { LibrosService } from './libros.service';

describe('LibrosService', () => {
  let service: LibrosService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(LibrosService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify()); // falla si quedó alguna petición sin responder

  it('manda el texto como parámetro y convierte la respuesta', () => {
    let resultado: Libro[] = [];
    service.buscar('borges').subscribe((libros) => (resultado = libros));

    const req = http.expectOne((r) => r.url === 'https://openlibrary.org/search.json');
    expect(req.request.params.get('q')).toBe('borges');
    expect(req.request.params.get('limit')).toBe('10');

    req.flush({
      numFound: 2,
      docs: [
        { key: '/works/1', title: 'Ficciones', author_name: ['Jorge Luis Borges'], first_publish_year: 1944 },
        { key: '/works/2', title: 'Sin datos' },
      ],
    });

    expect(resultado).toEqual([
      { id: '/works/1', titulo: 'Ficciones', autores: ['Jorge Luis Borges'], anio: 1944 },
      { id: '/works/2', titulo: 'Sin datos', autores: [], anio: null },
    ]);
  });
});
