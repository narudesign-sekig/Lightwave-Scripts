@script modeler
@version 2.6
@name "SK_SurfToLayerPart"

//=======================================================
// SK_SurfToLayerPart.ls
//
// revision	: 1.00
// date		: 2012-05-24
// author	: naru design [ http://narudesign.com ]
//=======================================================

main
{
	flagLayerName = recall("layer", true);
	flagPartsName = recall("parts", true);

	reqbegin("SurfToLayerParts (c)2012 naru desgin");
	reqsize(380, 120);

    c1 = ctlcheckbox("Set Layer Name to Surface Name",flagLayerName);
    ctlposition(c1, 30, 20);

    c2 = ctlcheckbox("Set Parts Name to Surface Name",flagPartsName);
    ctlposition(c2, 30, 52);

	if(reqpost()) {

		flagLayerName = getvalue(c1);
		flagPartsName = getvalue(c2);
		
		selmode(DIRECT);
		selpolygon(CLEAR);
		
		nofSurf = 1;
		currSurf = nextsurface();
		while(currSurf != nil) {
			currSurf = nextsurface(currSurf);
			nofSurf++;
		}
		
		moninit(nofSurf, "Processing...");
		
		workLayer = lyrfg();						// get current layer
		
		currSurf = nextsurface();					// get surface
		while(currSurf != nil) {
			
			if(monstep()) {
				break;
			}
			
			selpolygon(SET, SURFACE, currSurf);		// select polygon specified surface
			polyCnt = polycount();
			
			if(polyCnt[1]) {
				emptyLyr = lyrempty();				// get empty layer
				if(flagPartsName) {
					changepart(currSurf);				// change part name (selected poly)
				}
				cut();								// cut polygon
				lyrsetfg(emptyLyr[1]);				// chage to empty layer
				if(flagLayerName) {
					setlayername(currSurf);				// change layer name
				}
				paste();							// paste polygon
			}
			
			currSurf = nextsurface(currSurf);		// get next surface
			lyrsetfg(workLayer);					// select init layer
		}
	}
}
