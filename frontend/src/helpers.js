import {Observable} from 'rxjs/Observable'
import 'rxjs/add/observable/interval'
import 'rxjs/add/observable/from'
import 'rxjs/add/observable/timer'
import 'rxjs/add/observable/forkJoin'
import 'rxjs/add/operator/map'
import 'rxjs/add/operator/mergeMap'
import 'rxjs/add/operator/zip'
import L from 'leaflet'

export function maxProp (obj) {
  let maxKey = ''
  let maxVal = -Infinity
  Object.keys(obj).forEach(key => {
    if (obj[key] > maxVal) {
      maxVal = obj[key]
      maxKey = key
    }
  })
  return maxKey
}

export const PARTY_COLORS = {
  afd: '#2B9FDB',
  gruene: '#4E8935',
  spd: '#DB0E2A',
  cdu: '#000000',
  fdp: '#FEE943',
  die_linke: '#CC008A'
}

export const BWK_NAMES = {
  '075': 'Mitte',
  '076': 'Pankow',
  '077': 'Reinickendorf',
  '078': 'Spandau',
  '079': 'Steglitz/Zehlendorf',
  '080': 'Charlottenburg/Wilmersdorf',
  '081': 'Tempelhof/Schöneberg',
  '082': 'Neukölln',
  '083': 'Friedrichshain/Kreuzb.',
  '084': 'Treptow/Köpenick',
  '085': 'Marzahn/Hellersdorf',
  '086': 'Lichtenberg'
}

export function minAwait (observable, timeout = 500) {
  const timeoutOb = Observable.timer(500)
  return Observable.forkJoin(observable, timeoutOb).map(arr => arr[0])
}

export function asyncChunks (inputData, period, chunkSize = 50) {
  const chunks = []
  for (let i = 0; i < inputData.length; i += chunkSize) {
    chunks.push(inputData.slice(i, i + chunkSize))
  }
  return Observable.from(chunks).zip(Observable.interval(period), function (a, b) {
    return a
  }).mergeMap(function (chunk) {
    return Observable.from(chunk)
  })
}

const tileLayerAPI = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}'
const accessToken = 'pk.eyJ1IjoibmVtb25lc3N1bm8iLCJhIjoiY2phM3FvbGRkM2x6MTM0cGN1M3h6dHcyYiJ9.Gie5hDNbis60D17BFvH31Q'

export function buildLeafletMap (element) {
  if (!element) {
    console.warn('buildLeafletMap() received undefined as argument')
  }
  const tileLayer = L.tileLayer(tileLayerAPI, {
    attribution: `Map data &copy;
    <a href="http://openstreetmap.org">
      OpenStreetMap
    </a>
    contributors,
    <a href="http://creativecommons.org/licenses/by-sa/2.0/">
      CC-BY-SA
    </a>, Imagery ©
    <a href="http://mapbox.com">Mapbox</a>`,
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken
  })
  return L.map(element, {
    center: [52.5200, 13.4050],
    zoom: 10,
    maxzoom: 13,
    doubleClickZoom: false,
    zoomControl: false,
    layers: [tileLayer]
  })
}
