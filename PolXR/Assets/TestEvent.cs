using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class TestEvent : MonoBehaviour
{
    // Start is called before the first frame update

    public GameObject lineObj;

    void Start()
    {
        BoxCollider collider = lineObj.AddComponent<BoxCollider>();

        lineObj.AddComponent<XRGrabInteractable>();

        XRGrabInteractable m_Interactable = lineObj.GetComponent<XRGrabInteractable>();
        // m_Interactable.firstSelectEntered.AddListener(TogglePolyline);
    }

    void TogglePolyline(SelectEnterEventArgs args)
    {
        IXRSelectInteractable component = args.interactableObject;
        IXRSelectInteractor interactor = args.interactorObject;

        Debug.Log("in here");
        component.transform.gameObject.SetActive(false);
    }
}
