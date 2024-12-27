using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class Events
{
    public void CloseMainMenu()
    {
        GameObject.Find("MainMenu").SetActive(false);
    }

    public void CloseRadarMenu()
    {
        GameObject.Find("RadarMenu").SetActive(false);
    }
}
