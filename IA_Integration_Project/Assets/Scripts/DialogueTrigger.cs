using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.EventSystems;

public class DialogueTrigger : MonoBehaviour
{
    [Header("References")]
    public GameObject player;
    public GameObject dialogueUI;
    public TMP_InputField inputField;
    public Button sendButton;
    public MonoBehaviour movementScript;
    public GameObject interactionPromptText; // Objeto UI compartido (Dialogue_Activator)

    [Header("Settings")]
    public float triggerDistance = 3f;

    private bool isDialogueActive = false;
    private bool isPlayerInRange = false;

    private ChatMessage chatMessage;
    private BillboardFollower billboardFollower;
    private TMP_Text promptLabel;
    private NPCIdentity npcIdentity;

    void Start()
    {
        if (dialogueUI != null)
        {
            chatMessage = dialogueUI.GetComponent<ChatMessage>();
            if (chatMessage == null)
                Debug.LogWarning("No se encontró ChatMessage en el UI de diálogo.");
        }

        if (interactionPromptText != null)
        {
            billboardFollower = interactionPromptText.GetComponent<BillboardFollower>();
            promptLabel = interactionPromptText.GetComponentInChildren<TMP_Text>();
        }

        npcIdentity = GetComponent<NPCIdentity>();
        if (npcIdentity == null)
            Debug.LogWarning("No se encontró NPCIdentity en " + gameObject.name);
    }

    void Update()
    {
        if (!AllReferencesAssigned())
            return;

        float distance = Vector3.Distance(transform.position, player.transform.position);
        isPlayerInRange = distance <= triggerDistance;

        if (isPlayerInRange && !isDialogueActive)
        {
            DialogueManager.Instance?.RequestInteractionPrompt(this);
        }
        else
        {
            DialogueManager.Instance?.ClearInteractionPrompt(this);
        }

        if (isPlayerInRange && !isDialogueActive && Input.GetKeyDown(KeyCode.T))
        {
            ActivateDialogue();
        }

        if (isDialogueActive)
        {
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                EventSystem.current.SetSelectedGameObject(null);
                DeactivateDialogue();
            }

            if (Input.GetKeyDown(KeyCode.Return))
            {
                sendButton.onClick.Invoke();
            }
        }
    }

    void ActivateDialogue()
    {
        isDialogueActive = true;
        dialogueUI.SetActive(true);
        interactionPromptText.SetActive(false);

        if (chatMessage != null && chatMessage.chatText != null)
        {
            chatMessage.chatText.text = "";
        }

        inputField.ActivateInputField();
        movementScript.enabled = false;

        Cursor.lockState = CursorLockMode.None;
        Cursor.visible = true;

        if (chatMessage != null && npcIdentity != null)
        {
            chatMessage.SetCurrentNPC(npcIdentity.npcName);
        }
    }

    void DeactivateDialogue()
    {
        isDialogueActive = false;
        dialogueUI.SetActive(false);
        movementScript.enabled = true;

        if (isPlayerInRange)
            DialogueManager.Instance?.RequestInteractionPrompt(this);

        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }

    public void ShowInteractionPrompt(bool show)
    {
        interactionPromptText.SetActive(show);

        if (billboardFollower != null && show)
            billboardFollower.SetTarget(transform);

        if (promptLabel != null && show)
            promptLabel.text = $"Pulsa T para hablar con {npcIdentity?.npcName ?? "NPC"}";
    }

    bool AllReferencesAssigned()
    {
        return player != null &&
               dialogueUI != null &&
               inputField != null &&
               sendButton != null &&
               movementScript != null &&
               interactionPromptText != null &&
               npcIdentity != null;
    }
}
