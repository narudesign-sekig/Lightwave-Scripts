@script modeler
@version 2.6
@name "SelNextBGLayer"

//=======================================================
// SK_SelNextBGLayer.ls
//
// revision	: 1.00
// date		: 2013-09-09
// author	: naru design [ http://narudesign.com ]
//=======================================================

main
{
	// get foreground and background layer
	
	backgroundLayer = lyrbg();
	foregroundLayer = lyrfg();

	if(backgroundLayer.size() != 1) {
		error("Invalid layer selection. Select one bg layer.");
		return;
	}
	
	bg = backgroundLayer[1];
	bg++;
	while(!checkLayer(bg, foregroundLayer))
	{
		bg++;
	}
	lyrsetbg(bg);
}

checkLayer: lay, flay
{
	for(i = 1; i <= flay.size(); i++)
	{
		if(lay == flay[i]) return(false);
	}	
	return(true);
}


