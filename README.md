# VISER: XR scientific visualization tool for ice-penetrating radar data in Antarctica and Greenland

This application facilitates the analysis of radar data for polar geophysicists by using Extended Reality (XR) technology to visualize radar returns in an accurate 3D geospatial context.

Project Website: https://pgg.ldeo.columbia.edu/projects/VISER

_Note: This project is still in development_.

***Last Updated 10/31/2024.***

# Team

Developers:
* [Qazi Ashikin](https://github.com/qaziashikin), Columbia University
* [Anusha Lavanuru](), Columbia University
* [Leah Kim](https://github.com/LEAAHKIM), Barnard College
* [Moises Mata](), Columbia University
* [Linda Mukarakate](), Barnard College
* [Greg Ou](), Columbia University
* [Joel Salzman](https://github.com/joelsalzman), Columbia University
* [Ben Yang](https://github.com/benplus1), Columbia University
  
Additional Contributors:
* [Isabel Cordero](https://lamont.columbia.edu/directory/s-isabel-cordero), Lamont-Doherty Earth Observatory
* [Andrew Hoffman](https://lamont.columbia.edu/directory/andrew-o-hoffman), Lamont-Doherty Earth Observatory
* [Carmine Elvezio](https://carmineelvezio.com/), Columbia University
* [Bettina Schlager](https://www.cs.columbia.edu/~bschlager/), Columbia University

Advisors:
* Dr. [Robin Bell](https://pgg.ldeo.columbia.edu/people/robin-e-bell), Lamont-Doherty Earth Observatory
* Dr. [Alexandra Boghosian](https://alexandraboghosian.com/), Lamont-Doherty Earth Observatory
* Dr. [Kirsty Tinto](https://pgg.ldeo.columbia.edu/people/kirsty-j-tinto), Lamont-Doherty Earth Observatory
* Professor [Steven Feiner](http://www.cs.columbia.edu/~feiner/), Columbia University

<br />

# Background

Ice-penetrating radar is a powerful tool to study glaciological processes but the data are often difficult to interpret. These radar measurements are taken by flying a plane equipped with sensors along some path (known as the flightline) and plotting the radar returns. These plots (radargrams) must be interpreted, often manually, in order to distinguish features inside the ice. Glaciologists are intensely interested in identifying the ice surface, bedrock depth, and whatever features can be discerned in the subsurface. An essential step in this process is "picking lines," or identifying contiguous curves in radargrams that correspond to real features in the world (as opposed to noise). Current methods are suboptimal.

VISER aims to improve interpretability of radargrams using XR. First, we place the user inside a digital twin of the relevant ice shelf so that all the data are properly contextualized relative to each other in space. Second, we model the radargrams as Unity GameObjects so that the features visible on the plots (which appear as textures on the GameObjects) also appear in the proper 3D geospatial context. Third, we implement numerous interfaces for analysis and manipulation so that users can explore the data.

# Project Architecture

The application contains three scenes.

* Home Menu
* Ross Ice Shelf (RIS)
* Petermann Glacier (PG or Petermann)

The Home Menu scene is mostly empty except for an XR menu that allows users to load one of the other scenes.
<img src="https://github.com/qaziashikin/polAR/blob/Summer/images/homeMenu.png?raw=true"      alt="Home Menu"      style="float: left; margin-right: 10px;" />
<br />

### Ross Ice Shelf (RIS) Scene

The RIS scene uses the following assets.
| Asset Name | Source | Description |
| :-----------: | ----------- | ----------- |
| Surface DEM | BedMachine | Digital elevation model of ice shelf surface |
| Base DEM | BedMachine | Digital elevation model of bedrock |
| Radar Images | ROSETTA | Planar GameObjects textured with radargrams |
| CSV Picks Containers | ROSETTA | Points on the flightlines |
| Minimap |  | Aerial map that lives on the scene menu and allows users to teleport |
| Bounding Box |  | Bounding box around the entire scene |
| Grid |  | Evenly-spaced graticule grid generated at runtime |

In this scene, radar images are textured on planar GameObjects. Only plots from the portions of the flightline where the plane was flying relatively straight are shown. This scene has the most mature navigation system and includes a minimap.

The flightlines are loaded from CSV files as discrete points.

<img src="https://github.com/qaziashikin/polAR/blob/Summer/images/ris_sceneMenu.png?raw=true"      alt="RIS Scene Menu"      style="float: left; margin-right: 10px;" />
<br />

### Petermann Glacier Scene

The Petermann scene uses the following assets.
| Asset Name | Source | Description |
| :-----------: | ----------- | ----------- |
| Surface DEM | BedMachine | Digital elevation model of glacier surface |
| Base DEM | BedMachine | Digital elevation model of bedrock |
| Flightlines | IceBridge (CReSis) | Polylines corresponding to where the plane flying the radar system went above the surface |
| Radargram meshes | IceBridge (CReSis) | Triangle meshes with radargrams mapped as texture |
| Bounding Box |  | Bounding box around the entire scene |
| Grid |  | Evenly-spaced graticule grid generated at runtime |

<img src="https://github.com/qaziashikin/polAR/blob/Summer/images/petermann_sceneMenu.png?raw=true"      alt="Petermann Scene Menu"      style="float: left; margin-right: 10px;" />
<br />

In this scene, the flightlines and radargrams are generated at runtime as GameObjects rather than living permanently in the scene. The flightlines are rendered as polylines and are broken up into segments during preprocessing. Each radar object is modeled as a triangle mesh, textured with a radargram, and linked to the associated flightline portion. Using meshes enables the entire flightline to be displayed. The flightline coordinates are accurate within the projected coordinate system but the vertical coordinate is snapped to the surface DEM for ease of viewing.

<img src="https://github.com/qaziashikin/polAR/images/blob/Summer/petermann_screenshot.png?raw=true"      alt="Petermann DEM-Radar Intersection"      style="float: left; margin-right: 10px;" />
<br />

The radargram objects are generated in the following way. In preprocessing, the plots are generated in MATLAB and converted into the three separate files by the _greenland_obj.m_ script.

* .obj (contains the geometry of the mesh)
* .mtl (the material file for the mesh)
* .png (the radargram; this is mapped onto the mesh)

The .obj files then need to be decimated in order to improve performance. This is done in Blender and currently requires manual attention to ensure that the meshes do not deform significantly at the boundaries. These simplified .obj files, along with the .mtl and .png files, are added to the Assets folder. Upon loading the scene, the _LoadFlightlines.cs_ script programmatically generates meshes from the file triples and associates each textured mesh with the corresponding flightline polyline. Users can select a flightline portion to load a mesh.

<br />

<details>
<summary><strong>Scene Workflows</strong></summary>

<br />

<details>
<summary><strong>RIS Scene Workflow</strong></summary>

---
### Ross Ice Shelf (RIS) Workflow

1.  **Scene Load:** User selects the RIS scene from the Home Menu.
2.  **Data Loading (`CSVReadPlot.cs`):**
    * Reads flightline data from CSV files located in `Resources/SplitByLine...`.
    * Creates `ParticleSystem` GameObjects to represent the flightline points.
    * Loads DEM models (`Bedmap2_surface_RIS`, `Bedmap2_bed`) from `Resources/Prefabs`.
    * Reads radar image position/scale data from `Resources/RadarInfoPosScale.csv`.
    * Instantiates planar GameObjects (`RadarImagePlane` prefab) for each radar image at the specified positions/scales. Initially, these might have a default white texture.
3.  **Scene Setup (`CSVReadPlot.cs`, `DrawGrid.cs`):**
    * Associates the `ParticleSystem` flightlines with the corresponding planar radar GameObjects via `RadarEvents2D.SetLine()`.
    * Instantiates and configures DEM GameObjects.
    * `DrawGrid.cs` generates the background graticule.
    * Minimap elements are initialized (`MinimapControl.cs`).
4.  **User Interaction:**
    * User interacts with the scene using VR controllers.
    * **Selection:** Selecting a radar plane (`GameObject` with `RadarEvents2D.cs`) triggers texture loading (`RadarEvents2D.loadImage()`) for that specific radargram and synchronizes the Radar Menu (`RadarEvents.SychronizeMenu()`).
    * **Manipulation:** User can manipulate the radar plane (scale, rotate) via the Radar Menu (interactions likely handled by the now mostly commented-out `MenuEvents.cs` or potentially UI elements directly calling `RadarEvents2D` methods).
    * **Measurement:** Toggling Measurement Mode allows placing `MarkObj` and `MeasureObj` (`RadarEvents2D.OnPointerDown`), with `UpdateLine.cs` drawing the line between them.
    * **Navigation:** User moves via joystick teleportation or uses the Minimap (`MinimapControl.cs`) for larger jumps.
    * **Toggles:** Main Menu allows toggling visibility of all radar images, all CSV picks, DEMs, etc. (handled by UI elements calling methods in `CSVReadPlot` or potentially `MenuEvents`).

---
</details>

<details>
<summary><strong>Petermann Scene Workflow</strong></summary>

---
### Petermann Glacier (PG) Workflow

1.  **Scene Load:** User selects the Petermann scene from the Home Menu.
2.  **Data Loading (`DataLoader.cs`):**
    * Reads DEM `.obj` files from the directory specified in the editor (`Assets/AppData/DEMs/...`).
    * Reads Flightline `.obj` files from specified directories (`Assets/AppData/Flightlines/...`).
    * Reads Radargram `.obj` (mesh) and `.png` (texture) files from specified directories (`Assets/AppData/Flightlines/...`).
3.  **Scene Setup (`DataLoader.cs`, `DrawGrid.cs`):**
    * Instantiates DEM GameObjects from loaded `.obj` files.
    * Instantiates Flightline GameObjects for each segment:
        * Creates `LineRenderer` components from `.obj` vertices.
        * Attaches `BoxCollider`s and `XRSimpleInteractable` components.
        * Attaches `FlightlineInfo.cs` to store metadata (e.g., `isBackwards`).
    * Instantiates Radargram GameObjects for each segment:
        * Applies the loaded `.obj` mesh and `.png` texture (using `RadarShader.shader`).
        * Adds `MeshCollider` and `XRGrabInteractable` components for interaction.
        * Scales and rotates objects appropriately.
        * Radargram meshes are typically set to inactive initially.
    * `DrawGrid.cs` generates the background graticule.
    * Sets up UI listeners for toggles and buttons on MainMenu and RadarMenu canvases.
4.  **User Interaction:**
    * User interacts with the scene using VR controllers.
    * **Selection:** Selecting a Flightline segment (via `XRSimpleInteractable`) triggers a listener (configured in `DataLoader.cs`) that likely calls `RadarEvents3D.ToggleRadar()` on the corresponding Radargram object, making the mesh visible/invisible. Selecting the Flightline might also change its color and open the Radar Menu.
    * **Manipulation:** Grabbing a visible Radargram mesh (via `XRGrabInteractable`) allows the user to move and rotate it. `RadarEvents3D` manages state synchronization (e.g., with the Radar Menu).
    * **Line Picking:**
        * User enables Line Picking mode (e.g., via a button handled by `ToggleLinePickingMode.cs`).
        * User points at a radargram mesh and presses the trigger.
        * `PickLine.cs` detects the interaction, uses `UVHelpers.cs` to calculate the hit UV coordinate and then trace a path along the brightest pixels (or based on gradient) on the texture.
        * `PickLine.cs` draws the traced path using a `LineRenderer`.
        * Picked line data (pixel coordinates and world coordinates) can be saved via `RadarEvents3D.saveRadargram()`.
    * **UI Interaction:** Using toggles/buttons on the MainMenu or RadarMenu triggers listeners set up by `DataLoader.cs` to perform actions like toggling DEM visibility, toggling all flightlines, opening/closing menus, resetting radargram transforms (`RadarEvents3D.ResetTransform`), etc.

---
</details>

---
</details>

<br />

### Code files

| Filename | Description | Scenes |
| :-----------: | ----------- | ----------- |
| HomeMenuEvents | Handles events in the Home Menu scene | Home |
| CSVReadPlot | Reads flightlines from CSV files into the scene | RIS |
| HoverLabel | Manages on-the-fly radar image tickmarks | RIS |
| MinimapControl | Controls the minimap | RIS |
| UpdateLine | Redraws the line between the Mark and Measure objects | RIS |
| RadarEvents2D | Handles events specific to the (2D) radargram planes | RIS |
| LoadFlightLines | Generates radargram meshes from obj/mtl files | Petermann |
| Measurement | Calculates distances used in Measurement Mode | Petermann |
| RadarEvents3D | Handles events specific to the (3D) radargram meshes | Petermann |
| DrawGrid | Generates a graticule grid in the scene | RIS, Petermann |
| DynamicLabel | Manages on-the-fly radar menu updates | RIS, Petermann |
| MarkObj | Handles events associated with the mark (cursor) object | RIS, Petermann |
| MenuEvents | Handles generic events associated with menus | RIS, Petermann |
| RadarEvents | Handles events associated with radargrams that are the same in both scenes | RIS, Petermann |

<details>
<summary><strong>Click here for Detailed Script Descriptions & Additional Scripts</strong></summary>

*(Note: This table includes scripts found in the 'Scripts' folder, including some not originally listed, and provides more detail. Descriptions may reflect current functionality observed in code over original intent where applicable.)*

| Filename             | Description                                                                                                                                                                                                                       | Scenes             |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| **DataLoader.cs** | Loads DEM and Flightline data (.obj, .png) from specified directories at runtime. Creates GameObjects, applies textures/materials, adds interaction components (`XRGrabInteractable`), and configures UI events for menus.                  | Petermann          |
| **DataLoaderEditor.cs**| Custom Unity Editor script to provide a more user-friendly interface (dropdowns) for selecting DEM and Flightline data directories in the Inspector for `DataLoader.cs`.                                                            | Editor Only        |
| HomeMenuEvents       | Handles scene loading events triggered by buttons in the Home Menu scene.                                                                                                                                                           | Home               |
| CSVReadPlot          | Reads flightlines from CSV files and plots them as `ParticleSystem`. Loads planar radar images and DEMs from `Resources`. Used in the RIS scene workflow.                                                                             | RIS                |
| HoverLabel           | Manages the display of temporary labels (tickmarks) when hovering over radar images.                                                                                                                                              | RIS                |
| MinimapControl       | Controls the minimap display, camera position/view, and user position marker. Handles teleportation via minimap interaction (though interaction code might be currently commented out).                                             | RIS                |
| UpdateLine           | Redraws the `LineRenderer` connecting the `MarkObj` and `MeasureObj` GameObjects when in Measurement Mode.                                                                                                                       | RIS                |
| RadarEvents          | Base class providing common properties and methods for radar objects (2D and 3D), such as getting scale, setting alpha, and synchronizing with the menu.                                                                           | RIS, Petermann     |
| RadarEvents2D        | Inherits from `RadarEvents`. Handles events specific to the 2D planar radargrams in the RIS scene, including texture loading, toggling visibility, managing associated CSV line (`ParticleSystem`), and handling measurement interactions. | RIS                |
| RadarEvents3D        | Inherits from `RadarEvents`. Handles events specific to the 3D radargram meshes in the Petermann scene, including toggling mesh/flightline visibility, selection handling, transformations, line picking data processing/saving.         | Petermann          |
| Measurement          | Calculates distances between `MarkObj` and `MeasureObj` for Measurement Mode. Contains logic related to coordinate systems (EPSG). Some functionality might be commented out.                                                   | Petermann (primarily) |
| DrawGrid             | Generates a graticule grid in the scene using `LineRenderer` based on specified parameters.                                                                                                                                      | RIS, Petermann     |
| DynamicLabel         | Manages dynamic updates for labels, often used for axis tickmark labels associated with `MarkObj`, adjusting position and text based on parent scale.                                                                            | RIS, Petermann     |
| MarkObj              | Handles the behavior and appearance of the 2D mark/cursor object, including its visual representation (circle, axes) and axis labels (`DynamicLabel`).                                                                             | RIS, Petermann     |
| MarkObj3D            | Handles the behavior and appearance of the 3D mark/cursor object used with 3D radargram meshes. Manages visual elements like the circle renderer.                                                                                 | Petermann          |
| MenuEvents           | Intended to handle generic menu events (sliders, toggles, buttons). *Note: Most functionality appears commented out in the current code; `DataLoader.cs` seems to handle many UI setup tasks now.* | RIS, Petermann     |
| CameraController     | Sets the initial position of the main camera based on the DEM's centroid calculated by `DataLoader`.                                                                                                                              | Petermann (likely) |
| ConsoleToGUI         | Utility script for displaying Unity console log messages onto a UI Text element for debugging purposes.                                                                                                                             | Debug/Utility      |
| Events               | Contains simple methods for closing the MainMenu and RadarMenu GameObjects.                                                                                                                                                        | Utility            |
| FlightlineInfo       | Simple component attached to Flightline objects to store metadata, specifically whether the flightline data runs backward (`isBackwards`). Used by `UVHelpers`.                                                                    | Petermann          |
| MinimapFollowUser    | Makes the user's position marker on the minimap follow the main camera's position and adds a blinking effect.                                                                                                                     | RIS                |
| Mode                 | Defines an enum (`Snap`, `Free`) likely intended for different object manipulation modes (currently seems unused).                                                                                                                | Utility            |
| PalmUpDetection      | Detects if the user's palm is facing upwards (based on wrist transform) to potentially show/hide a menu canvas.                                                                                                                  | Utility            |
| PreserveRadargrams   | Singleton script to persist selected radargram GameObjects between scene loads (e.g., from Petermann to a dedicated 'Study' scene).                                                                                                | Utility            |
| RadialMenu           | Part of a radial menu system, likely handling the main menu logic, selection state, and cursor position based on input (`touchPosition`).                                                                                        | Utility            |
| RadialSelection      | Represents a single selectable item in the `RadialMenu`, holding an icon and an event to trigger on selection.                                                                                                                    | Utility            |
| SnapRadargramManager | Manages the selection of radargrams (up to 6) for a 'Study Scene'. Converts 3D radargram textures to UI Sprites for display in a scrollable list and handles loading the 'StudyScene'.                                              | Petermann          |
| StudySceneManager    | Runs in the 'StudyScene' to retrieve and display the radargrams persisted by `PreserveRadargrams`.                                                                                                                                 | StudyScene         |
| **LinePicking/PickLine.cs** | Core script for the line picking feature. Detects user input on radargram meshes, initiates the picking process using `UVHelpers`, and draws the resulting line.                                                              | Petermann (likely) |
| **LinePicking/ToggleLinePickingMode.cs** | Enables/disables the line picking mode based on user input and adjusts controller ray visuals accordingly.                                                                                                   | Petermann (likely) |
| **LinePicking/UVHelpers.cs** | Utility script containing core logic for line picking: calculates UV coordinates from hits, finds line paths based on texture data, converts UV to 3D world coordinates. Relies on `GeometryUtils` and `TextureUtils`.      | Petermann (likely) |
| **LinePicking/TextureUtils.cs** | Utility functions for texture manipulation used in line picking: reflecting textures, saving debug textures, getting pixel brightness.                                                                                | Petermann (likely) |
| **LinePicking/GeometryUtils.cs** | Provides geometric helper functions (triangle area, closest point on triangle, barycentric coordinates) used by `UVHelpers`.                                                                                           | Petermann (likely) |
| *LoadFlightLines (Unused)* | *Originally listed as generating radargram meshes. Appears superseded by `DataLoader.cs` and is located in the 'Unused' folder.* | *Obsolete* |

</details>

<br />

# Controls

VISER works on both AR (Hololens) and VR (Quest) headsets. Since the most recent version is optimized for VR, we omit the AR controls in this section.

### Universal Controls 

Here is a list of interactions available everywhere using the Oculus Controllers:

| Interaction | Description |
| :-----------: | ----------- |
| Trigger Buttons | Used to interact with the menus and select radar images |
| Joysticks | Used to move around the entire scene freely |

Movement can be accomplished with the joysticks. Tilt forward to shoot a ray; if the ray is white, release the joystick to teleport there. You can also nudge yourself back by tilting back on the joystick.

The scene bounding box can be used to scale everything inside the scene along any of the three axes. Users can grab the bounding box from the corners or the center of any edge and use standard MRTK manipulation to adjust the box's size.

Here is a list of interactions available with the main menu. All of these interactions can be used with the Oculus Controller trigger buttons:
| Main Menu Interaction Title | Description |
| :-----------: | ----------- |
| Surface DEM | Checking this button turns the Surface DEM on/off |
| Base DEM | Checking this button turns the Base DEM on/off |
| Bounding Box | Checking this button turns the bounding box for the entire scene on/off |
| Vertical Exaggeration | Vertically stretches or shrinks the DEMs (the exaggeration is dynamic and can be repeated limitlessly) |
| Sidebar "X" | Closes the menu |
| Sidebar "Refresh" | Resets the entire scene |
| Sidebar "Pin" | Saves scene information to .txt file; currently non-functional |

<br />

### RIS Scene Controls

Because the Ross Ice Shelf scene uses a different workflow than the Petermann Glacier scene, some of the controls are different. Here are the menu options that are only available in the RIS scene.

<img src="https://github.com/qaziashikin/polAR/blob/Summer/images/ris_radarMenu.png?raw=true"      alt="RIS Radar Menu"      style="float: left; margin-right: 10px;" />
<br />

| Main Menu Interaction Title | Description |
| :-----------: | ----------- |
| All Radar Images | Checking this button turns all the radar lines on/off |
| All CSV Picks | Checking this button turns all the CSV Picks on/off |
| Sidebar "Minimap" | Turns teleport mode on (dot will be green) or off (dot will be red and allows for moving the minimap) |
| Minimap | If teleport mode is enabled, teleports the user to that location in the scene |

Here is a list of interactions available with the line menu. All of these interactions can be used with the Oculus Controller trigger buttons:
| Line Menu Interaction Title | Description |
| :-----------: | ----------- |
| Vertical Exaggeration | Vertically stretches or shrinks the radar image (the exaggeration is dynamic and can be repeated limitlessly) |
| Horizontal Exaggeration | Horizontally stretches or shrinks the radar image (the exaggeration is dynamic and can be repeated limitlessly) |
| Rotation | Rotates the image by the seleced amount of degrees |
| Transparency | Makes the radar image transparent by the selected percent |
| View Radar Image | Checking this button turns the selected radar image on/off |
| View CSV Picks | Checking this button turns the selected CSV Picks on/off |

The line menu has a unique sidebar.
| Main Menu Interaction Title | Description |
| :-----------: | ----------- |
| Measurement Mode | Turns measurent mode on/off (allows user to place two marks on the same image and measure the distance between) |
| Sidebar "X" | Closes the menu |
| Sidebar "Home" | Opens the main menu |
| Sidebar "Refresh" | Resets the radar line, or snap two radar images under measure mode |
| Sidebar "Pin" | Saves
