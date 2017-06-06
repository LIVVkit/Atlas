;***********************************************
; ISMIP6 Atlas function
; Plot diagnostic model output
; Heiko Goelzer Nov 2016 (hgoelzer@uu.nl)
;
; Usage: ncl -Q <Arguments> gland_fun.ncl

; Arguments
;  print(afile)
;  print(aexp)
;  print(avar)
;  print(atsp)
;  print(apal)
;  print(amod)
;  print(amin)
;  print(amax)
;  print(alsp)
;  print(alvl)
;  print(alabel)

begin

  ; add a netcdf file 
  f     = addfile(afile,"r")
  ; time step
  nt    = atsp
  ; get variable from file
  data  := f->$avar$(nt,:,:)

  ; array size
  dimgrd= dimsizes(data)
  ny  = dimgrd(0)
  nx  = dimgrd(1)

  ; aspect ratio
  asp = int2flt(nx)/int2flt(ny)

  ; Open png for graphics.
  wks = gsn_open_wks("png",aexp+"_"+avar+"_"+alabel)   

  ; Plot setting
  res                      = True
  ; Maximize plot in frame
  res@gsnMaximize          = True          
  ; Match grid aspect ratio
  res@vpWidthF      = asp
  res@vpHeightF     = 1.0

  res@cnFillOn             = True          ; Turn on contour fill
  res@cnFillMode           = "RasterFill"  ; Turn on raster fill
  res@cnLinesOn            = False         ; Turn on/off contour lines

; Color map and mapping options
  res@cnFillPalette = apal
  res@cnConstFEnableFill = True
  if(amod .eq. 0) then
    ; automatic levels
    res@cnLevelSelectionMode = "AutomaticLevels"
  else if(amod .eq. 1) then
    ; manual levels range (and step)
    res@cnLevelSelectionMode = "ManualLevels"
    res@cnMinLevelValF       =  amin
    res@cnMaxLevelValF       =  amax
    if((alsp .ne. 0) ) then
      res@cnLevelSpacingF      =  alsp
    end if  
  else if(amod .eq. 2) then
    ; explicit contour levels
    res@cnLevelSelectionMode = "ExplicitLevels"   
    res@cnLevels    = alvl
  end if  
  end if
  end if

  res@lbOrientation        = "vertical"

  ; Grid point numbers  
  res@sfXArray = fspan(1,nx,nx)
  res@sfYArray = fspan(1,ny,ny)

  ; Labels
  res@txFontHeightF   = 0.013
  res@tiMainString    = ""
  res@tiXAxisString   = ""
  res@tiYAxisString   = ""

  ; Ticks
  res@tmYLOn = False
  res@tmYROn = False
  res@tmXTOn = False
  res@tmXBOn = False

  ; Tick labels off
  res@tmYLLabelsOn = False
  res@tmXBLabelsOn = False
  
  ; Plot  
  contour = gsn_csm_contour(wks,data,res)

end
