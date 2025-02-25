//Keeps track of the save status of the page
//Global
import { writable } from 'svelte/store';

export const saveStatus = writable<string>('Page Up to Date');
export let isArchitectureSaved = writable<boolean>(true); 