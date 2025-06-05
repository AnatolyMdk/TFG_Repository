using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BillboardFollower : MonoBehaviour
{
    public Transform target; // El NPC a seguir
    public Vector3 offset = new Vector3(0, 2f, 0); // Altura sobre la cabeza

    private RectTransform rectTransform;

    void Start()
    {
        rectTransform = GetComponent<RectTransform>();
    }

    void Update()
    {
        if (target == null) return;

        Vector3 screenPos = Camera.main.WorldToScreenPoint(target.position + offset);

        if (screenPos.z < 0)
        {
            rectTransform.gameObject.SetActive(false);
            return;
        }

        rectTransform.gameObject.SetActive(true);
        rectTransform.position = screenPos;
    }

    public void SetTarget(Transform newTarget)
    {
        target = newTarget;
    }
}
