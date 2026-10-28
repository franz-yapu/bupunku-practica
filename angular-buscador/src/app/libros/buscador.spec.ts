import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Buscador } from './buscador';

const URL = 'https://openlibrary.org/search.json';
const respuesta = { numFound: 1, docs: [{ key: '/works/1', title: 'Ficciones' }] };

describe('Buscador', () => {
  let fixture: ComponentFixture<Buscador>;
  let componente: Buscador;
  let http: HttpTestingController;

  beforeEach(() => {
    vi.useFakeTimers(); // controlamos el reloj para el debounce de 300 ms
    TestBed.configureTestingModule({
      imports: [Buscador],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    fixture = TestBed.createComponent(Buscador);
    componente = fixture.componentInstance;
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify();
    vi.useRealTimers();
  });

  function escribir(texto: string) {
    componente.busqueda.setValue(texto);
    vi.advanceTimersByTime(300);
  }

  it('no busca con menos de 3 letras', () => {
    escribir('bo');
    http.expectNone(() => true);
  });

  it('espera 300 ms: una sola petición aunque se escriba rápido', () => {
    componente.busqueda.setValue('bor');
    vi.advanceTimersByTime(100);
    componente.busqueda.setValue('borg');
    vi.advanceTimersByTime(100);
    componente.busqueda.setValue('borges');
    vi.advanceTimersByTime(300);

    const req = http.expectOne((r) => r.url === URL);
    expect(req.request.params.get('q')).toBe('borges');
    req.flush(respuesta);
  });

  it('switchMap cancela la búsqueda anterior', () => {
    escribir('borges');
    const vieja = http.expectOne((r) => r.params.get('q') === 'borges');

    escribir('cortazar');
    const nueva = http.expectOne((r) => r.params.get('q') === 'cortazar');

    expect(vieja.cancelled).toBe(true);
    nueva.flush(respuesta);
    expect(componente.total()).toBe(1);
  });

  it('muestra el error en pantalla y la siguiente búsqueda sigue funcionando', () => {
    escribir('borges');
    http.expectOne((r) => r.url === URL).error(new ProgressEvent('error'));

    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('No se pudo conectar');

    escribir('cortazar');
    http.expectOne((r) => r.url === URL).flush(respuesta);

    fixture.detectChanges();
    expect(componente.error()).toBeNull();
    expect(fixture.nativeElement.textContent).toContain('1 resultados');
    expect(fixture.nativeElement.textContent).toContain('Ficciones');
  });
});
