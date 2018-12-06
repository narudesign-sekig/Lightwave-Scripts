@script modeler
@version 2.6
@name "SelPrevBGLayer"

//=======================================================
// SK_SelPrevBGLayer.ls
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
	newbg = bg;
	if(newbg == 1) return;
	
//	debug();

	i = newbg - 1;
	while(i > 0)
	{
		if(checkLayer(i, foregroundLayer))
		{
			newbg = i;
			break;
		}
		i--;
	}
	lyrsetbg(newbg);
}

checkLayer: lay, flay
{
	for(i = 1; i <= flay.size(); i++)
	{
		if(lay == flay[i]) return(false);
	}	
	return(true);
}
