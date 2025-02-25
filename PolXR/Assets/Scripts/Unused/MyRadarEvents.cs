using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MyRadarEvents : MonoBehaviour
{
    private void ToggleRadar(bool state)
    {
        foreach (Transform child in transform)
        {
            if (child.name.StartsWith("Data"))
            {
                child.gameObject.SetActive(!child.gameObject.activeSelf);
            }
        }
    }
}
