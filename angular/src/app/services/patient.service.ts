import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Patient } from '../definitions/patient';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PatientService {

  private currentUrl = localStorage.getItem('url')
  private PatientsUrl = this.currentUrl + 'patients';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  
  /**
   * Handle Http operation that failed.
   * Let the app continue. 
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
  
  private log(message: string) {
    this.messageService.add(`PatientService: ${message}`);
  }
  
  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }


  /** GET Patients from the server */
  getAllPatients(currPage: number, pageSize: number): Observable<any> {
    const url = `${this.PatientsUrl}?currPage=${currPage + 1}&pageSize=${pageSize}`
    return this.http.get<any>(url)
      .pipe(
        tap(response => this.log(response.query)),
        catchError(this.handleError<any>('getPatients', []))
      );
  }

  /* GET Patients whose id contains search term */
  searchPatients(term: string): Observable<Patient[]> {
    if (!term.trim()) {
      // if not search term, return empty Patient array.
      return of([]);
    }
    return this.http.get<any>(`${this.PatientsUrl}?id=${term}`).pipe(
      tap(response => this.log(response.query)),
      map(res => res.patients),
      catchError(this.handleError<any>('searchPatients', []))
    );
  }
  
  /** POST: add a new Patient to the server */
  createPatient(Patient: Patient): Observable<any> {
    return this.http.post<any>(this.PatientsUrl, Patient, this.httpOptions).pipe(
      tap(response => this.log(response.query)),
      catchError(this.handleError<any>('createPatient'))
    );
  }

  /** GET Patient by id. Will 404 if id not found */
  getPatient(id: number): Observable<Patient> {
    const url = `${this.PatientsUrl}/${id}`;
    return this.http.get<any>(url).pipe(
      tap(response => this.log(response.query)),
      map(res => res.patient),
      catchError(this.handleError<any>(`getPatient id=${id}`))
    );
  }

  /** PUT: update the Patient on the server */
  updatePatient(id: number, Patient: Patient): Observable<any> {
    return this.http.put<any>(`${this.PatientsUrl}/${id}`, Patient, this.httpOptions)
      .pipe(
        tap(response => this.log(response.query)),
        catchError(this.handleError<any>('updatePatient'))
      );
  }

  /** DELETE: delete the Patient from the server */
  deletePatient(id: number): Observable<any> {
    const url = `${this.PatientsUrl}/${id}`;
    return this.http.delete<any>(url, this.httpOptions).pipe(
      tap(response => this.log(response.query)),
      catchError(this.handleError<any>('deletePatient'))
    );
  }

}
