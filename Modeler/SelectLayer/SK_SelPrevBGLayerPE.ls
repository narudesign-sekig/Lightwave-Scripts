@script modeler
@version 2.6
@name "SelPrevBGLayerPE"

//=======================================================
// SK_SelPrevBGLayerPE.ls
//
// revision	: 1.00
// date		: 2013-09-26
// author	: naru design [ http://narudesign.com ]
//=======================================================

main
{
	// get foreground and background layer
	
	backgroundLayer = lyrbg();
	foregroundLayer = lyrfg();
	dataLayer = lyrdata();
	dataLayer.sortA();
	
	if(backgroundLayer.size() != 1) {
		error("Invalid layer selection. Select one bg layer.");
		return;
	}
	
	bg = backgroundLayer[1];
	
	for(i = dataLayer.size(); i > 0; i--)
	{
		if(bg > dataLayer[i])
		{
			if(!isForegroundLayer(dataLayer[i], foregroundLayer))
			{
				bg = dataLayer[i];
				lyrsetbg(bg);
				break;
			}
		}
	}
}

isForegroundLayer: lay, flay
{
	for(i = 1; i <= flay.size(); i++)
	{
		if(lay == flay[i]) return(true);
	}	
	return(false);
}
