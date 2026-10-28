export interface DocumentoOpenLibrary {
  key: string;
  title: string;
  author_name?: string[];
  first_publish_year?: number;
}

export interface RespuestaBusqueda {
  numFound: number;
  docs: DocumentoOpenLibrary[];
}

export interface Libro {
  id: string;
  titulo: string;
  autores: string[];
  anio: number | null;
}