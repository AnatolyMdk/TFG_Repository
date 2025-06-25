using UnityEngine;

public class DialogueManager : MonoBehaviour
{
    public static DialogueManager Instance;

    private void Awake()
    {
        if (Instance != null && Instance != this)
            Destroy(gameObject);
        else
            Instance = this;
    }

    public DialogueTrigger currentTrigger;

    public void RequestInteractionPrompt(DialogueTrigger requester)
    {
        if (currentTrigger == null || requester == currentTrigger)
        {
            currentTrigger = requester;
            requester.ShowInteractionPrompt(true);
        }
        else
        {
            requester.ShowInteractionPrompt(false);
        }
    }

    public void ClearInteractionPrompt(DialogueTrigger requester)
    {
        if (currentTrigger == requester)
        {
            requester.ShowInteractionPrompt(false);
            currentTrigger = null;
        }
    }
}
