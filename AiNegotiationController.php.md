<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class AiNegotiationController extends Controller
{
    private $aiBaseUrl = "https://ai-negotiation-staging.onrender.com";

    // Step 1: Start session
    public function startSession(Request $request)
    {
        $response = Http::post($this->aiBaseUrl . "/web/session/start", [
            "name" => $request->name,
            "phone_number" => $request->phone_number,
            "product_id" => $request->product_id,
            "language" => "en"
        ]);

        return response()->json($response->json());
    }

    // Step 2: Send message
    public function sendMessage(Request $request)
    {
        $response = Http::post($this->aiBaseUrl . "/messages/", [
            "session_id" => $request->session_id,
            "sender" => "customer",
            "message" => $request->message
        ]);

        return response()->json($response->json());
    }
}
