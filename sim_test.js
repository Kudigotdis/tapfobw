const qs = `
const PROMOS_DATA = {
  "Clothing": ["PROMOS/Clothing/test1.jpg", "PROMOS/Clothing/test2.jpg"]
};
const MEDIUMS_DATA = {
  "Radio": ["MEDIUMS/Radio/test1.jpg", "MEDIUMS/Radio/test2.jpg"]
};

const state = {
  promoPanelIdx: 0,
  selectedPromoMainCat: "Clothing"
};

const cat = state.selectedPromoMainCat;
const manifestKey = cat.replace(/ /g, '_').replace(/&/g, '').replace(/__/g, '_');

const isMediums = state.promoPanelIdx === 2;
const manifestName = isMediums ? 'mediums_manifest' : 'promos_manifest';
const fallbackData = isMediums 
  ? (typeof MEDIUMS_DATA !== 'undefined' ? MEDIUMS_DATA : null) 
  : (typeof PROMOS_DATA !== 'undefined' ? PROMOS_DATA : null);
const stateKey = isMediums ? 'mediumsManifest' : 'promosManifest';

if (!state[stateKey]) {
  if (fallbackData) {
    state[stateKey] = fallbackData;
  }
}

const activeManifest = state[stateKey];
const promoPaths = activeManifest[manifestKey] ||
  activeManifest[cat.replace(/ & /g, '_').replace(/ /g, '_')] ||
  [];

console.log("Weekly 'Clothing':", promoPaths);

// Now for mediums
state.promoPanelIdx = 2;
state.selectedPromoMainCat = "Radio";

const cat2 = state.selectedPromoMainCat;
const manifestKey2 = cat2.replace(/ /g, '_').replace(/&/g, '').replace(/__/g, '_');

const isMediums2 = state.promoPanelIdx === 2;
const fallbackData2 = isMediums2 
  ? (typeof MEDIUMS_DATA !== 'undefined' ? MEDIUMS_DATA : null) 
  : (typeof PROMOS_DATA !== 'undefined' ? PROMOS_DATA : null);
const stateKey2 = isMediums2 ? 'mediumsManifest' : 'promosManifest';

if (!state[stateKey2]) {
  if (fallbackData2) {
    state[stateKey2] = fallbackData2;
  }
}

const activeManifest2 = state[stateKey2];
const promoPaths2 = activeManifest2[manifestKey2] ||
  activeManifest2[cat2.replace(/ & /g, '_').replace(/ /g, '_')] ||
  [];

console.log("Mediums 'Radio':", promoPaths2);
`;
eval(qs);
