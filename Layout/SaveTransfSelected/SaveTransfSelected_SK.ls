@version 2.5
@script generic
@name SaveTransfSelected_SK
generic
{
    objlist=Scene().getSelect();
    
    if(!objlist || size(objlist)<2)
    {
        error("You must multi-select some meshes to export.");
        return;
    }
    
    objdir=string(getdir(CONTENTDIR), "/SaveTransfSelected_SK_TMP/");
    chdir(getdir(CONTENTDIR));
    if(!fileexists(objdir))
        mkdir(objdir);
        
    for(i=size(objlist); i>=1; i--)
    {
	    objlist[i].select();
        SaveTransformed(objdir + "/" + i + ".lwo");
    }
}
