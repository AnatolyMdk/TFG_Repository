using UnityEngine;
using TMPro;

public class IntroTextManager : MonoBehaviour
{
    public GameObject introPanel;       // Referencia al panel con el texto
    public float displayTime = 6f;      // Tiempo que se muestra antes de ocultarse

    void Start()
    {
        introPanel.SetActive(true);
        Invoke(nameof(HideIntro), displayTime);
    }

    void HideIntro()
    {
        introPanel.SetActive(false);
    }
}
