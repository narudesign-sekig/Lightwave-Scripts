@script modeler
@version 2.6
@name "SwapLayerWN"

//=======================================================
// SK_SwapLayerWN.ls
//
// revision	: 1.00
// date		: 2012-05-25
// author	: naru design [ http://narudesign.com ]
//=======================================================

main
{
	// get foreground and background layer
	
	foregroundLayer = lyrfg();
	backgroundLayer = lyrbg();

/*	
	info("fore " + foregroundLayer[1] + ", size() : " + foregroundLayer.size());
	info("back " + backgroundLayer[1] + ", size() : " + backgroundLayer.size());
*/
	
	if((foregroundLayer.size() != 1) || (backgroundLayer.size() != 1)) {
		error("Invalid layers selection");
		return;
	}
	
	mesh = Mesh() || error("No Object Loaded!");
	
	foregroundLayerName = mesh.layerName(foregroundLayer[1]);
	backgroundLayerName = mesh.layerName(backgroundLayer[1]);

/*	
	info(mesh.layerName(foregroundLayer[1]));
	info(mesh.layerName(backgroundLayer[1]));
*/
	
	emptyLayers = lyrempty();	// get empty layers
	if( (emptyLayers[1] == foregroundLayer[1]) || (emptyLayers[1] == backgroundLayer[1]) ) {
		emptyLayer = emptyLayers[2];
	} else {
		emptyLayer = emptyLayers[1];
	}
//	info(emptyLayer[1]);
	
//	debug();
	
	selmode(USER);
	
	// foreground layer -> empty layer
	
	if(backgroundLayerName) {
		setlayername(backgroundLayerName);
	} else {
		setlayername();
	}
	cut();
	lyrsetfg(emptyLayer);
	paste();

	// background layer -> foreground layer
	
	lyrsetfg(backgroundLayer[1]);
	if(foregroundLayerName) {
		setlayername(foregroundLayerName);
	} else {
		setlayername();
	}
	
	cut();
	lyrsetfg(foregroundLayer[1]);
	paste();
	
	// empty layer -> background layer
	
	lyrsetfg(emptyLayer);
	cut();
	lyrsetfg(backgroundLayer[1]);
	paste();
	
	lyrsetbg(foregroundLayer[1]);
}
