@script modeler
@version 2.6
@name "SK_PolySendBGLayer"

//=======================================================
// SK_PolySendBGLayer.ls
//
// revision	: 1.00
// date		: 2012-12-08
// author	: naru design [ http://narudesign.com ]
//=======================================================

main
{
	// get foreground and background layer
	
	foregroundLayer = lyrfg();
	backgroundLayer = lyrbg();

	if((foregroundLayer.size() < 1) || (backgroundLayer.size() != 1)) {
		error("Invalid layers selection");
		return;
	}
	
	selmode(DIRECT);
	
	cut();
	
	lyrswap();
//	lyrsetfg(backgroundLayer[1]);
	
	paste();
	
	lyrswap();
//	lyrsetfg(foregroundLayer[1]);
//	lyrsetbg(backgroundLayer[1]);
	
}
