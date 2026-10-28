// Lo que DEVUELVE la API (no lo controlamos: nombres en inglés, campos opcionales)
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

// Lo que USA nuestra app (lo controlamos: nombres claros, sin opcionales)
export interface Libro {
  id: string;
  titulo: string;
  autores: string[];
  anio: number | null;
}
