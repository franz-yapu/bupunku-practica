import { Component, inject, OnInit } from '@angular/core';
import { LibrosService,LibrosResponse } from './libros.service';

@Component({
  imports: [],
  selector: 'app-libros',
  styleUrl: './libros.css',
  templateUrl: './libros.html',
})
export class Libros implements OnInit {
   private service: LibrosService = inject(LibrosService);
   public librosData: LibrosResponse = {
    numFound: 0,
    start: 0,
    docs: []
  };

constructor( ) {}

  ngOnInit() {
 /*    this.getlibros(); */
  
  }




  /* getlibros() {
    this.service.getLibros(item: string).subscribe({
        next: (data: LibrosResponse) => {
            this.librosData = data;
            console.log('Libros data (Observable):', data);
        },
        error: (error) => {
            console.error('Error fetching libros (Observable):', error);
        }
    });
  }
 */




}