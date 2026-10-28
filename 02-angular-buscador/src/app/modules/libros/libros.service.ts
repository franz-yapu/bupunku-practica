import { Inject, Injectable } from "@angular/core";
import { environment } from "../../../environments/environment";
import { Observable } from "rxjs";

export interface LibrosResponse {
    numFound: number;
    start: number;
    docs: Array<{
        title: string;
        author_name?: string[];
        first_publish_year?: number;
        cover_i?: number;
    }>;
}


@Injectable({
    providedIn: 'root'
})
export class LibrosService {
    private baseUrl: string = environment.backend;
    constructor() { }

    async getLibros() {
        try {
            const response = await fetch(`${this.baseUrl}/search.json?q=TEXTO&limit=10`);
            return await response.json() as LibrosResponse;
        } catch (error) {
            console.error('Error fetching libros:', error);
            throw error;
        }
    }

     getLibros2():Observable<LibrosResponse> {
        return new Observable<LibrosResponse>((observer) => {
            fetch(`${this.baseUrl}/search.json?q=TEXTO&limit=10`)
                .then(response => response.json())
                .then(data => {
                    observer.next(data as LibrosResponse);
                    observer.complete();
                })
                .catch(error => {
                    console.error('Error fetching libros:', error);
                    observer.error(error);
                });
        });
    }
}
